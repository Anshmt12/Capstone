"""Indian Constitution - Key provisions chunked for vector DB ingestion."""

CONSTITUTION_CHUNKS = [
    {
        "text": "Article 14 - Equality before law: The State shall not deny to any person equality before the law or the equal protection of the laws within the territory of India. This is a fundamental right guaranteed under Part III of the Constitution of India. The Supreme Court has interpreted Article 14 to include the concept of reasonable classification, which permits differentiation if it is based on intelligible differentia having a rational nexus with the object sought to be achieved.",
        "metadata": {"source": "Indian Constitution", "article": "14", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 19 - Protection of certain rights regarding freedom of speech, etc.: (1) All citizens shall have the right (a) to freedom of speech and expression; (b) to assemble peaceably and without arms; (c) to form associations or unions; (d) to move freely throughout the territory of India; (e) to reside and settle in any part of the territory of India; (g) to practise any profession, or to carry on any occupation, trade or business. These rights are subject to reasonable restrictions under Article 19(2) to 19(6).",
        "metadata": {"source": "Indian Constitution", "article": "19", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 21 - Protection of life and personal liberty: No person shall be deprived of his life or personal liberty except according to procedure established by law. The Supreme Court in Maneka Gandhi v. Union of India (1978) expanded Article 21 to include the right to live with dignity, right to livelihood, right to health, right to clean environment, right to education, right to privacy, and right to shelter among others. This article is the most litigated fundamental right.",
        "metadata": {"source": "Indian Constitution", "article": "21", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 32 - Remedies for enforcement of fundamental rights: (1) The right to move the Supreme Court by appropriate proceedings for the enforcement of the rights conferred by this Part is guaranteed. (2) The Supreme Court shall have power to issue directions or orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari, whichever may be appropriate, for the enforcement of any of the rights conferred by this Part. Dr. B.R. Ambedkar called Article 32 the 'heart and soul' of the Constitution.",
        "metadata": {"source": "Indian Constitution", "article": "32", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 15 - Prohibition of discrimination on grounds of religion, race, caste, sex or place of birth: (1) The State shall not discriminate against any citizen on grounds only of religion, race, caste, sex, place of birth or any of them. (3) Nothing in this article shall prevent the State from making any special provision for women and children. (4) Nothing shall prevent the State from making any special provision for the advancement of any socially and educationally backward classes of citizens or for the Scheduled Castes and the Scheduled Tribes.",
        "metadata": {"source": "Indian Constitution", "article": "15", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 20 - Protection in respect of conviction for offences: (1) No person shall be convicted of any offence except for violation of a law in force at the time of the commission of the act charged as an offence, nor be subjected to a penalty greater than that which might have been inflicted under the law in force at the time of the commission of the offence. (2) No person shall be prosecuted and punished for the same offence more than once. (3) No person accused of any offence shall be compelled to be a witness against himself.",
        "metadata": {"source": "Indian Constitution", "article": "20", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 22 - Protection against arrest and detention in certain cases: (1) No person who is arrested shall be detained in custody without being informed, as soon as may be, of the grounds for such arrest nor shall he be denied the right to consult, and to be defended by, a legal practitioner of his choice. (2) Every person who is arrested and detained in custody shall be produced before the nearest magistrate within a period of twenty-four hours of such arrest.",
        "metadata": {"source": "Indian Constitution", "article": "22", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 25 - Freedom of conscience and free profession, practice and propagation of religion: (1) Subject to public order, morality and health and to the other provisions of this Part, all persons are equally entitled to freedom of conscience and the right freely to profess, practise and propagate religion. (2) Nothing in this article shall affect the operation of any existing law or prevent the State from making any law (a) regulating or restricting any economic, financial, political or other secular activity which may be associated with religious practice.",
        "metadata": {"source": "Indian Constitution", "article": "25", "part": "III", "category": "Fundamental Rights"},
    },
    {
        "text": "Article 44 - Uniform civil code for the citizens: The State shall endeavour to secure for the citizens a uniform civil code throughout the territory of India. This is a Directive Principle of State Policy under Part IV. The Supreme Court has on multiple occasions urged the Parliament to implement a Uniform Civil Code, including in Shah Bano case (1985) and Sarla Mudgal v. Union of India (1995).",
        "metadata": {"source": "Indian Constitution", "article": "44", "part": "IV", "category": "Directive Principles"},
    },
    {
        "text": "Article 226 - Power of High Courts to issue certain writs: (1) Every High Court shall have powers to issue to any person or authority, including the Government, directions, orders or writs, including writs in the nature of habeas corpus, mandamus, prohibition, quo warranto and certiorari for the enforcement of any of the rights conferred by Part III and for any other purpose. This is broader than Article 32 as it can be invoked for any legal right, not just fundamental rights.",
        "metadata": {"source": "Indian Constitution", "article": "226", "part": "V", "category": "High Courts"},
    },
    {
        "text": "Article 300A - Right to property: No person shall be deprived of his property save by authority of law. Originally Article 19(1)(f) and Article 31 guaranteed the right to property as a fundamental right. The 44th Amendment Act, 1978 removed it from the list of fundamental rights and inserted Article 300A as a constitutional right. The State can acquire private property but must follow due process and provide compensation as per the statute.",
        "metadata": {"source": "Indian Constitution", "article": "300A", "part": "XII", "category": "Property Rights"},
    },
    {
        "text": "Article 141 - Law declared by Supreme Court to be binding on all courts: The law declared by the Supreme Court shall be binding on all courts within the territory of India. This establishes the doctrine of precedent (stare decisis) in the Indian legal system. All High Courts and subordinate courts are bound by the ratio decidendi of Supreme Court judgments.",
        "metadata": {"source": "Indian Constitution", "article": "141", "part": "V", "category": "Supreme Court"},
    },
    {
        "text": "Article 142 - Enforcement of decrees and orders of Supreme Court: (1) The Supreme Court in the exercise of its jurisdiction may pass such decree or make such order as is necessary for doing complete justice in any cause or matter pending before it. This extraordinary power allows the Supreme Court to fashion remedies that may not be available under any statute, and has been used in landmark cases for environmental protection, human rights, and institutional reform.",
        "metadata": {"source": "Indian Constitution", "article": "142", "part": "V", "category": "Supreme Court"},
    },
    {
        "text": "Article 265 - Taxes not to be imposed save by authority of law: No tax shall be levied or collected except by authority of law. This is a fundamental principle of Indian taxation law. Any imposition of tax without legislative backing is unconstitutional and void. The authority of law means a valid law enacted by a competent legislature following proper legislative procedure.",
        "metadata": {"source": "Indian Constitution", "article": "265", "part": "XII", "category": "Taxation"},
    },
    {
        "text": "Article 368 - Power of Parliament to amend the Constitution and procedure therefor: Parliament may in exercise of its constituent power amend by way of addition, variation or repeal any provision of this Constitution. However, the Supreme Court in Kesavananda Bharati v. State of Kerala (1973) held that Parliament cannot alter the basic structure of the Constitution. The basic structure doctrine includes supremacy of the Constitution, republican and democratic form of government, secular character, separation of powers, and federal character.",
        "metadata": {"source": "Indian Constitution", "article": "368", "part": "XX", "category": "Amendment"},
    },
    {
        "text": "Section 302 of the Indian Penal Code (now Section 103 of Bharatiya Nyaya Sanhita 2023) - Punishment for murder: Whoever commits murder shall be punished with death, or imprisonment for life, and shall also be liable to fine. Murder is defined where the act is done with the intention of causing death, or with the intention of causing bodily injury known to be likely to cause death, or with the knowledge that the act is so imminently dangerous that it must in all probability cause death or such bodily injury as is likely to cause death.",
        "metadata": {"source": "Indian Penal Code / BNS", "section": "302/103", "category": "Criminal Law"},
    },
    {
        "text": "Section 420 of the Indian Penal Code (now Section 318 of Bharatiya Nyaya Sanhita 2023) - Cheating and dishonestly inducing delivery of property: Whoever cheats and thereby dishonestly induces the person deceived to deliver any property to any person, or to make, alter or destroy the whole or any part of a valuable security, or anything which is signed or sealed, shall be punished with imprisonment which may extend to seven years, and shall also be liable to fine.",
        "metadata": {"source": "Indian Penal Code / BNS", "section": "420/318", "category": "Criminal Law"},
    },
    {
        "text": "Section 498A of the Indian Penal Code (now Section 85 of Bharatiya Nyaya Sanhita 2023) - Husband or relative of husband of a woman subjecting her to cruelty: Whoever, being the husband or the relative of the husband of a woman, subjects such woman to cruelty shall be punished with imprisonment for a term which may extend to three years and shall also be liable to fine. Cruelty includes both physical and mental harassment, especially related to dowry demands.",
        "metadata": {"source": "Indian Penal Code / BNS", "section": "498A/85", "category": "Criminal Law"},
    },
    {
        "text": "Vishaka v. State of Rajasthan (1997) - Sexual Harassment Guidelines: The Supreme Court laid down guidelines to prevent sexual harassment at workplace, known as the Vishaka Guidelines. These were binding until the enactment of the Sexual Harassment of Women at Workplace (Prevention, Prohibition and Redressal) Act, 2013. The court used Article 14, 19(1)(g), and 21 along with CEDAW to formulate these guidelines, establishing that sexual harassment violates fundamental rights to equality and life with dignity.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Vishaka v. State of Rajasthan", "year": "1997", "category": "Landmark Judgment"},
    },
    {
        "text": "Kesavananda Bharati v. State of Kerala (1973) - Basic Structure Doctrine: In this landmark 13-judge bench decision, the Supreme Court held that while Parliament has wide powers to amend the Constitution under Article 368, it cannot alter the 'basic structure' or framework of the Constitution. This includes the supremacy of the Constitution, rule of law, independence of judiciary, fundamental rights, secularism, federalism, and free and fair elections.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Kesavananda Bharati v. State of Kerala", "year": "1973", "category": "Landmark Judgment"},
    },
    {
        "text": "Maneka Gandhi v. Union of India (1978) - Expanded scope of Article 21: The Supreme Court held that the procedure established by law under Article 21 must be fair, just and reasonable, not arbitrary or oppressive. This overruled A.K. Gopalan v. State of Madras (1950) which had given a narrow interpretation to Article 21. The court held that Articles 14, 19 and 21 are interconnected and a law depriving personal liberty must satisfy all three articles.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Maneka Gandhi v. Union of India", "year": "1978", "category": "Landmark Judgment"},
    },
    {
        "text": "K.S. Puttaswamy v. Union of India (2017) - Right to Privacy: A nine-judge bench of the Supreme Court unanimously held that the right to privacy is a fundamental right protected under Articles 14, 19, and 21 of the Constitution. The court overruled M.P. Sharma v. Satish Chandra (1954) and Kharak Singh v. State of U.P. (1963) which had held that there is no fundamental right to privacy. This judgment has implications for data protection, surveillance, and personal autonomy.",
        "metadata": {"source": "Supreme Court Judgment", "case": "K.S. Puttaswamy v. Union of India", "year": "2017", "category": "Landmark Judgment"},
    },
    {
        "text": "Navtej Singh Johar v. Union of India (2018) - Decriminalization of homosexuality: The Supreme Court struck down Section 377 of the IPC insofar as it criminalized consensual sexual acts between adults of the same sex. The court held that Section 377 was violative of Articles 14, 15, 19, and 21. The judgment recognized sexual orientation as a natural and inherent aspect of a person's identity protected under the right to privacy and dignity.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Navtej Singh Johar v. Union of India", "year": "2018", "category": "Landmark Judgment"},
    },
    {
        "text": "Indian Evidence Act, 1872 (now Bharatiya Sakshya Adhiniyam 2023) - Section 3 defines evidence as including all statements which the Court permits or requires to be made before it by witnesses (oral evidence) and all documents including electronic records produced for the inspection of the Court (documentary evidence). Section 65B deals with the admissibility of electronic records and requires a certificate for the same. The Supreme Court in Arjun Panditrao Khotkar v. Kailash Kushanrao Gorantyal (2020) held that the certificate under Section 65B(4) is mandatory.",
        "metadata": {"source": "Indian Evidence Act / BSA", "section": "3, 65B", "category": "Evidence Law"},
    },
    {
        "text": "Code of Civil Procedure, 1908 - Order VII Rule 11 - Rejection of plaint: The plaint shall be rejected where it does not disclose a cause of action, where the relief claimed is undervalued and the plaintiff fails to correct within time, where it is written on insufficient stamp paper, or where the suit appears from the statement in the plaint to be barred by any law. The Supreme Court has held that the court should look at the averments in the plaint as a whole and decide whether they disclose a cause of action.",
        "metadata": {"source": "Code of Civil Procedure 1908", "section": "Order VII Rule 11", "category": "Civil Procedure"},
    },
    {
        "text": "Arbitration and Conciliation Act, 1996 - Section 34 provides for setting aside an arbitral award. An award can be challenged on grounds including incapacity of a party, invalid arbitration agreement, improper notice, the award dealing with disputes beyond the scope of submission, improper composition of tribunal, or the award being in conflict with the public policy of India. The Supreme Court in ONGC v. Saw Pipes (2003) interpreted 'public policy' broadly but this was narrowed in Ssangyong Engineering v. NHAI (2019).",
        "metadata": {"source": "Arbitration and Conciliation Act 1996", "section": "34", "category": "Arbitration Law"},
    },
    {
        "text": "Companies Act, 2013 - Section 241-242 - Prevention of oppression and mismanagement: Any member of a company who complains that the affairs of the company have been or are being conducted in a manner prejudicial to public interest or oppressive to any member may apply to the National Company Law Tribunal (NCLT) for relief. The NCLT has wide powers including regulation of company affairs, removal of directors, and restriction on transfer of shares.",
        "metadata": {"source": "Companies Act 2013", "section": "241-242", "category": "Corporate Law"},
    },
    {
        "text": "Right to Information Act, 2005 - Section 3: Subject to the provisions of this Act, all citizens shall have the right to information. Section 4 mandates every public authority to maintain records and publish information proactively. Section 8 lists exemptions including information affecting sovereignty and integrity of India, security, scientific or economic interests, cabinet papers, trade secrets, and personal privacy. Information relating to allegations of corruption cannot be denied.",
        "metadata": {"source": "Right to Information Act 2005", "section": "3, 4, 8", "category": "Information Law"},
    },
    {
        "text": "Protection of Women from Domestic Violence Act, 2005 - The Act provides civil remedies to women who are victims of domestic violence. Section 3 defines domestic violence broadly to include physical, sexual, verbal, emotional, and economic abuse. An aggrieved person can seek protection orders, residence orders, monetary relief, custody orders, and compensation orders. The Act recognizes domestic relationships including marriage, joint family living, and relationships in the nature of marriage.",
        "metadata": {"source": "Protection of Women from Domestic Violence Act 2005", "section": "3", "category": "Family Law"},
    },
    {
        "text": "Consumer Protection Act, 2019 - Replaced the 1986 Act. Establishes Consumer Disputes Redressal Commissions at District, State, and National levels. Introduces concepts of product liability, unfair contracts, and e-commerce regulations. Section 2(7) defines 'consumer' broadly to include any person who buys goods or hires services for consideration, including online transactions. The Act provides for mediation as an alternative dispute resolution mechanism.",
        "metadata": {"source": "Consumer Protection Act 2019", "section": "2(7)", "category": "Consumer Law"},
    },
    {
        "text": "Insolvency and Bankruptcy Code, 2016 - Section 7 allows financial creditors to initiate corporate insolvency resolution process (CIRP) against a corporate debtor by filing an application before the NCLT. Section 9 allows operational creditors to do the same. The timeline for resolution is 330 days including litigation time. The Supreme Court in Committee of Creditors of Essar Steel India v. Satish Kumar Gupta (2019) upheld the primacy of the Committee of Creditors in approving resolution plans.",
        "metadata": {"source": "Insolvency and Bankruptcy Code 2016", "section": "7, 9", "category": "Insolvency Law"},
    },
    {
        "text": "Article 48A - Protection and improvement of environment and safeguarding of forests and wild life: The State shall endeavour to protect and improve the environment and to safeguard the forests and wild life of the country. Read with Article 51A(g), which makes it a fundamental duty of every citizen to protect and improve the natural environment. The Supreme Court in M.C. Mehta v. Union of India cases has extensively used these provisions along with Article 21 to develop environmental jurisprudence.",
        "metadata": {"source": "Indian Constitution", "article": "48A", "part": "IV", "category": "Directive Principles"},
    },
    {
        "text": "Article 51A - Fundamental Duties: It shall be the duty of every citizen of India (a) to abide by the Constitution and respect its ideals; (b) to cherish and follow the noble ideals which inspired our national struggle for freedom; (c) to uphold and protect the sovereignty, unity and integrity of India; (e) to promote harmony and the spirit of common brotherhood; (f) to value and preserve the rich heritage of our composite culture; (g) to protect and improve the natural environment; (h) to develop the scientific temper; (j) to strive towards excellence in all spheres.",
        "metadata": {"source": "Indian Constitution", "article": "51A", "part": "IVA", "category": "Fundamental Duties"},
    },
    {
        "text": "Transfer of Property Act, 1882 - Section 54 defines 'sale' as a transfer of ownership in exchange for a price paid or promised. Section 58 deals with mortgage of immovable property. Section 105 defines 'lease' as a transfer of a right to enjoy property for a certain time in consideration of rent. The Act governs all transfers of immovable property between living persons and is fundamental to property law in India.",
        "metadata": {"source": "Transfer of Property Act 1882", "section": "54, 58, 105", "category": "Property Law"},
    },
    {
        "text": "Specific Relief Act, 1963 (as amended 2018) - Section 10 provides for specific performance of contracts relating to immovable property or where compensation would not be adequate relief. After the 2018 amendment, specific performance has become a general rule rather than an exception. Section 14 lists contracts that cannot be specifically enforced, including contracts for personal service and contracts too vague to be enforced.",
        "metadata": {"source": "Specific Relief Act 1963", "section": "10, 14", "category": "Contract Law"},
    },
    {
        "text": "Negotiable Instruments Act, 1881 - Section 138 deals with dishonour of cheques for insufficiency of funds. If a cheque is returned unpaid, the payee may send a demand notice within 30 days. If payment is not made within 15 days, the payee can file a criminal complaint within one month. The Supreme Court in Dashrath Rupsingh Rathod v. State of Maharashtra (2014) held that the complaint must be filed at the place where the cheque was dishonoured, but this was overruled by amendment.",
        "metadata": {"source": "Negotiable Instruments Act 1881", "section": "138", "category": "Banking Law"},
    },
    {
        "text": "Information Technology Act, 2000 - Section 43A mandates compensation for failure to protect sensitive personal data. Section 66 punishes computer-related offences. Section 66A was struck down by the Supreme Court in Shreya Singhal v. Union of India (2015) as unconstitutional. Section 69 empowers the government to intercept, monitor or decrypt information. Section 79 provides safe harbour to intermediaries subject to due diligence requirements.",
        "metadata": {"source": "Information Technology Act 2000", "section": "43A, 66, 69, 79", "category": "Cyber Law"},
    },
    {
        "text": "Motor Vehicles Act, 1988 (as amended 2019) - Chapter X deals with liability without fault in certain cases. Section 140 provides for no-fault liability where the owner or authorized driver must pay compensation for death or permanent disablement arising from motor vehicle accident regardless of fault. Section 163A provides structured formula for compensation. The 2019 amendment significantly increased penalties for traffic violations and introduced electronic enforcement.",
        "metadata": {"source": "Motor Vehicles Act 1988", "section": "140, 163A", "category": "Motor Vehicle Law"},
    },
    {
        "text": "Indian Contract Act, 1872 - Section 10: All agreements are contracts if they are made by the free consent of parties competent to contract, for a lawful consideration and with a lawful object, and are not expressly declared void. Section 23 specifies that the consideration or object of an agreement is unlawful if it is forbidden by law, defeats the provisions of any law, is fraudulent, involves injury to person or property, or is immoral or opposed to public policy.",
        "metadata": {"source": "Indian Contract Act 1872", "section": "10, 23", "category": "Contract Law"},
    },
    {
        "text": "Prevention of Corruption Act, 1988 (as amended 2018) - Section 7 punishes public servants for obtaining undue advantage. Section 7A punishes taking undue advantage to influence public servant. Section 8 punishes persons bribing public servants. The 2018 amendment introduced Section 17A requiring prior sanction for investigation of offences relatable to recommendations or decisions taken in official capacity. The Supreme Court has held that sanction is mandatory and its absence vitiates the prosecution.",
        "metadata": {"source": "Prevention of Corruption Act 1988", "section": "7, 7A, 8, 17A", "category": "Criminal Law"},
    },
    {
        "text": "Goods and Services Tax (GST) - Article 246A of the Constitution empowers both Parliament and State Legislatures to make laws with respect to GST. The GST Council under Article 279A makes recommendations on rates, exemptions, and model laws. The CGST Act, SGST Act, IGST Act, and UTGST Act form the legislative framework. Key provisions include input tax credit under Section 16 CGST Act, composition levy under Section 10, and anti-profiteering measures under Section 171.",
        "metadata": {"source": "Constitution / GST Acts", "article": "246A, 279A", "category": "Tax Law"},
    },
    {
        "text": "SEBI (Securities and Exchange Board of India) Act, 1992 - SEBI is the regulatory body for securities markets in India. Section 11 empowers SEBI to regulate securities markets, including registration and regulation of stock brokers, prohibiting insider trading and unfair trade practices. SEBI (Listing Obligations and Disclosure Requirements) Regulations, 2015 mandate disclosures by listed entities. SEBI (Prohibition of Insider Trading) Regulations, 2015 define connected persons and unpublished price sensitive information.",
        "metadata": {"source": "SEBI Act 1992", "section": "11", "category": "Securities Law"},
    },
    {
        "text": "M.C. Mehta v. Union of India (Oleum Gas Leak Case, 1987) - The Supreme Court developed the principle of absolute liability in India, going beyond the strict liability rule of Rylands v. Fletcher. The court held that where an enterprise is engaged in a hazardous or inherently dangerous activity and an accident occurs, the enterprise is absolutely liable to compensate all affected, regardless of whether due diligence was exercised. The larger the enterprise, the greater the compensation.",
        "metadata": {"source": "Supreme Court Judgment", "case": "M.C. Mehta v. Union of India (Oleum Gas Leak)", "year": "1987", "category": "Landmark Judgment"},
    },
    {
        "text": "Shreya Singhal v. Union of India (2015) - The Supreme Court struck down Section 66A of the Information Technology Act, 2000, which criminalized sending offensive messages through communication services. The court held that the provision was vague and overbroad, violating Article 19(1)(a) and not saved by Article 19(2). The court also read down Section 79 to require intermediaries to remove content only upon a court order.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Shreya Singhal v. Union of India", "year": "2015", "category": "Landmark Judgment"},
    },
    {
        "text": "S.R. Bommai v. Union of India (1994) - The nine-judge bench laid down important principles regarding imposition of President's Rule under Article 356. The court held that secularism is a basic feature of the Constitution, the President's proclamation under Article 356 is subject to judicial review, the power under Article 356 is to be exercised sparingly and as a last resort, and the floor test is the only way to determine whether a government commands majority.",
        "metadata": {"source": "Supreme Court Judgment", "case": "S.R. Bommai v. Union of India", "year": "1994", "category": "Landmark Judgment"},
    },
    {
        "text": "Indra Sawhney v. Union of India (1992) - Mandal Commission Case: The nine-judge bench upheld 27% reservation for Other Backward Classes (OBCs) but imposed a 50% ceiling on total reservations. The court excluded the 'creamy layer' among OBCs from reservation benefits. The court held that Article 16(4) is not an exception to Article 16(1) but a facet of it. Economic criterion alone cannot be the basis for reservation; social and educational backwardness must be considered.",
        "metadata": {"source": "Supreme Court Judgment", "case": "Indra Sawhney v. Union of India", "year": "1992", "category": "Landmark Judgment"},
    },
    {
        "text": "D.K. Basu v. State of West Bengal (1997) - The Supreme Court laid down 11 requirements to be followed in all cases of arrest or detention to prevent custodial violence and deaths. These include displaying name tags by arresting officers, preparing arrest memo with date and time, informing a friend or relative, medical examination every 48 hours, and right to meet a lawyer during interrogation. The court held that custodial torture violates Articles 21 and 22.",
        "metadata": {"source": "Supreme Court Judgment", "case": "D.K. Basu v. State of West Bengal", "year": "1997", "category": "Landmark Judgment"},
    },
    {
        "text": "Article 136 - Special leave to appeal by the Supreme Court: Notwithstanding anything in this Chapter, the Supreme Court may, in its discretion, grant special leave to appeal from any judgment, decree, determination, sentence or order in any cause or matter passed or made by any court or tribunal in the territory of India. This gives the Supreme Court overriding discretionary jurisdiction to entertain appeals from any court or tribunal. It is the widest appellate power vested in any court.",
        "metadata": {"source": "Indian Constitution", "article": "136", "part": "V", "category": "Supreme Court"},
    },
    {
        "text": "Limitation Act, 1963 - Prescribes time limits for filing suits, appeals, and applications. Article 113 provides a residuary period of 3 years for suits. Article 137 provides 3 years for applications. Section 5 allows condonation of delay if sufficient cause is shown. Section 14 excludes time spent prosecuting in good faith in a court without jurisdiction. The Supreme Court has held that limitation is a mixed question of law and fact.",
        "metadata": {"source": "Limitation Act 1963", "section": "5, 14, Article 113, 137", "category": "Limitation Law"},
    },
    {
        "text": "Real Estate (Regulation and Development) Act, 2016 (RERA) - Mandates registration of real estate projects and agents. Section 18 provides for return of amount with interest if the promoter fails to complete the project or deliver possession on time. The Real Estate Regulatory Authority adjudicates complaints. The Appellate Tribunal hears appeals. RERA was enacted to protect homebuyers and bring transparency and accountability in real estate transactions.",
        "metadata": {"source": "RERA 2016", "section": "18", "category": "Property Law"},
    },
    {
        "text": "Prevention of Money Laundering Act, 2002 (PMLA) - Section 3 defines money laundering as involvement in any process or activity connected with the proceeds of crime. Section 4 provides punishment up to 7 years (or 10 years for specified offences). Section 5 empowers the Enforcement Directorate to attach property involved in money laundering. The Supreme Court in Vijay Madanlal Choudhary v. Union of India (2022) upheld the constitutional validity of key PMLA provisions including the reverse burden of proof.",
        "metadata": {"source": "PMLA 2002", "section": "3, 4, 5", "category": "Criminal Law"},
    },
]
