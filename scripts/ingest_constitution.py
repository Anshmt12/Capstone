"""Ingest Indian legal documents into ChromaDB using Kaggle dataset."""
import os
import sys
import json
import kagglehub

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.rag.vector_store import add_documents, get_collection_stats, delete_collection

KAGGLE_DATASET = "akshatgupta7/llm-fine-tuning-dataset-of-indian-legal-texts"

# Minimum answer length to filter out stub answers like "Section 1 of Chapter I"
MIN_ANSWER_LENGTH = 30

# Landmark SC cases not in the Kaggle dataset — kept for citation accuracy
CASE_LAW_CHUNKS = [
    {
        "text": "K.S. Puttaswamy v. Union of India (2017) 10 SCC 1 - The Supreme Court declared that Right to Privacy is a fundamental right under Article 21. The nine-judge bench held that privacy is intrinsic to life and liberty and is inherently protected under various fundamental rights. This overruled previous judgments in M.P. Sharma and Kharak Singh that held privacy is not a fundamental right.",
        "metadata": {"source": "Supreme Court of India", "case_name": "K.S. Puttaswamy v. Union of India", "citation": "(2017) 10 SCC 1", "year": "2017", "category": "privacy"},
    },
    {
        "text": "Maneka Gandhi v. Union of India (1978) 1 SCC 248 - The Supreme Court expanded the scope of Article 21, holding that the procedure established by law must be fair, just and reasonable, not arbitrary. Articles 14, 19 and 21 are interconnected and any law affecting life or liberty must satisfy all three.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Maneka Gandhi v. Union of India", "citation": "(1978) 1 SCC 248", "year": "1978", "category": "due_process"},
    },
    {
        "text": "Kesavananda Bharati v. State of Kerala (1973) 4 SCC 225 - The Supreme Court propounded the Basic Structure Doctrine, holding that Parliament cannot amend the Constitution to destroy its basic features. Basic structure includes supremacy of Constitution, republican and democratic form of government, secular character, separation of powers, and federal character.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Kesavananda Bharati v. State of Kerala", "citation": "(1973) 4 SCC 225", "year": "1973", "category": "basic_structure"},
    },
    {
        "text": "Vishaka v. State of Rajasthan (1997) 6 SCC 241 - The Supreme Court laid down guidelines to prevent sexual harassment at workplace, binding until the Sexual Harassment of Women at Workplace Act, 2013 was enacted. Sexual harassment violates fundamental rights under Articles 14, 15, 19 and 21.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Vishaka v. State of Rajasthan", "citation": "(1997) 6 SCC 241", "year": "1997", "category": "sexual_harassment"},
    },
    {
        "text": "NALSA v. Union of India (2014) 5 SCC 438 - The Supreme Court recognized transgender persons as the third gender and held that they have fundamental rights under Articles 14, 15, 16, 19 and 21. The Court directed the government to treat them as socially and educationally backward classes.",
        "metadata": {"source": "Supreme Court of India", "case_name": "NALSA v. Union of India", "citation": "(2014) 5 SCC 438", "year": "2014", "category": "transgender_rights"},
    },
    {
        "text": "Navtej Singh Johar v. Union of India (2018) 10 SCC 1 - The Supreme Court decriminalized consensual homosexual acts between adults by reading down Section 377 of IPC. Section 377 violated Articles 14, 15, 19 and 21 to the extent it criminalized consensual sexual conduct between adults of the same sex.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Navtej Singh Johar v. Union of India", "citation": "(2018) 10 SCC 1", "year": "2018", "category": "lgbtq_rights"},
    },
    {
        "text": "D.K. Basu v. State of West Bengal (1997) 1 SCC 416 - The Supreme Court laid down 11 mandatory requirements to be followed in all cases of arrest or detention to prevent custodial violence: name tags on arresting officers, arrest memo with date/time, informing a friend or relative, medical examination every 48 hours, and right to meet a lawyer during interrogation.",
        "metadata": {"source": "Supreme Court of India", "case_name": "D.K. Basu v. State of West Bengal", "citation": "(1997) 1 SCC 416", "year": "1997", "category": "custodial_rights"},
    },
    {
        "text": "Indra Sawhney v. Union of India (1992) - Mandal Commission Case: The nine-judge bench upheld 27% reservation for OBCs but imposed a 50% ceiling on total reservations. The court excluded the creamy layer from OBC reservation benefits. Economic criterion alone cannot be the basis for reservation; social and educational backwardness must be considered.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Indra Sawhney v. Union of India", "citation": "(1992) Supp (3) SCC 217", "year": "1992", "category": "reservation"},
    },
    {
        "text": "S.R. Bommai v. Union of India (1994) 3 SCC 1 - Nine-judge bench: secularism is a basic feature of the Constitution. President's Rule under Article 356 is subject to judicial review and must be used as a last resort. The floor test is the only way to determine whether a government commands majority.",
        "metadata": {"source": "Supreme Court of India", "case_name": "S.R. Bommai v. Union of India", "citation": "(1994) 3 SCC 1", "year": "1994", "category": "federalism"},
    },
    {
        "text": "Shreya Singhal v. Union of India (2015) 5 SCC 1 - The Supreme Court struck down Section 66A of the IT Act as unconstitutional for violating Article 19(1)(a). The provision was vague and overbroad with a chilling effect on free speech online. Section 79 was read down to require court orders for intermediary takedowns.",
        "metadata": {"source": "Supreme Court of India", "case_name": "Shreya Singhal v. Union of India", "citation": "(2015) 5 SCC 1", "year": "2015", "category": "free_speech_online"},
    },
]

# Maps each Kaggle file to its ChromaDB metadata
DATASET_FILES = [
    {
        "filename": "constitution_qa.json",
        "source": "Constitution of India",
        "category": "constitution",
    },
    {
        "filename": "ipc_qa.json",
        "source": "Indian Penal Code",
        "category": "criminal_law",
    },
    {
        "filename": "crpc_qa.json",
        "source": "Code of Criminal Procedure",
        "category": "criminal_procedure",
    },
]


def load_kaggle_chunks(dataset_path: str) -> tuple[list[str], list[dict]]:
    """Load Q&A pairs from all Kaggle files and convert to RAG chunks."""
    texts, metadatas = [], []

    for file_cfg in DATASET_FILES:
        filepath = os.path.join(dataset_path, file_cfg["filename"])
        with open(filepath, encoding="utf-8") as f:
            entries = json.load(f)

        skipped = 0
        for entry in entries:
            question = entry.get("question", "").strip()
            answer = entry.get("answer", "").strip()

            # Skip stubs — short answers are usually bare section references
            if len(answer) < MIN_ANSWER_LENGTH:
                skipped += 1
                continue

            # Combine Q+A so semantic search matches both the question framing
            # and the answer content
            text = f"Q: {question}\nA: {answer}"
            metadata = {
                "source": file_cfg["source"],
                "category": file_cfg["category"],
                "question": question[:200],  # stored for debugging/display
            }
            texts.append(text)
            metadatas.append(metadata)

        loaded = len(entries) - skipped
        print(f"  {file_cfg['filename']}: {loaded} loaded, {skipped} skipped (short answers)")

    return texts, metadatas


def main():
    print("=" * 60)
    print("Ingesting Indian Legal Documents into ChromaDB")
    print("=" * 60)

    # Clear existing collection to avoid duplicates on re-run
    print("\nClearing existing ChromaDB collection...")
    delete_collection()
    print("Collection cleared.")

    # Download Kaggle dataset
    print(f"\nDownloading Kaggle dataset: {KAGGLE_DATASET}")
    dataset_path = kagglehub.dataset_download(KAGGLE_DATASET)
    print(f"Dataset path: {dataset_path}")

    # Load Kaggle chunks
    print("\nLoading dataset files...")
    kaggle_texts, kaggle_metadatas = load_kaggle_chunks(dataset_path)

    # Prepare landmark case chunks
    case_texts = [c["text"] for c in CASE_LAW_CHUNKS]
    case_metadatas = [c["metadata"] for c in CASE_LAW_CHUNKS]

    all_texts = kaggle_texts + case_texts
    all_metadatas = kaggle_metadatas + case_metadatas

    print(f"\nTotal chunks to ingest: {len(all_texts)}")
    print(f"  - Kaggle dataset (constitution + IPC + CrPC): {len(kaggle_texts)}")
    print(f"  - Landmark SC judgments (hardcoded): {len(case_texts)}")

    # Ingest in batches to show progress and avoid memory spikes
    batch_size = 500
    total = len(all_texts)
    ingested = 0

    print(f"\nIngesting in batches of {batch_size}...")
    for i in range(0, total, batch_size):
        batch_texts = all_texts[i : i + batch_size]
        batch_meta = all_metadatas[i : i + batch_size]
        add_documents(batch_texts, batch_meta)
        ingested += len(batch_texts)
        print(f"  Progress: {ingested}/{total} ({ingested * 100 // total}%)")

    stats = get_collection_stats()
    print(f"\nCollection stats:")
    print(f"  Name:      {stats['name']}")
    print(f"  Documents: {stats['count']}")
    print(f"  Location:  {stats['persist_directory']}")
    print("\n" + "=" * 60)
    print("Ingestion complete!")
    print("=" * 60)


if __name__ == "__main__":
    main()
