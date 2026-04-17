"""Seed the SQLite database with synthetic cases."""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.seed_cases import seed

if __name__ == "__main__":
    seed()
