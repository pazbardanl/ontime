from .di_config import get_query_resolver
from src.services.interfaces import QueryResolverInterface

def main(queryResolver: QueryResolverInterface):
    print(f'OnTime service running')
    queryResolver.resolve_user_query('Whatsup?')

if __name__ == "__main__":
    queryResolver = get_query_resolver()
    main(queryResolver)