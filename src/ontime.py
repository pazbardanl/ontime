from src.services import QueryResolver

def main():
    print(f'OnTime service running')
    queryResolver = QueryResolver()
    queryResolver.resolve_user_query('Whtasup?')

if __name__ == "__main__":
    main()