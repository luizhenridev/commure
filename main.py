from utils import (
    print_top_50_classical_players,
    print_last_30_day_rating_for_top_player,
    generate_rating_csv_for_top_50_classical_players
)

def main():
    print("Top 50 Classical Chess Players:")
    print_top_50_classical_players()
    print("\nLast 30 day rating for top player:")
    print_last_30_day_rating_for_top_player()
    print("\nGenerating CSV for top 50 players...")
    generate_rating_csv_for_top_50_classical_players()

if __name__ == "__main__":
    main()