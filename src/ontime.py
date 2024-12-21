from .di_config import get_query_resolver
from src.services.interfaces import QueryResolverInterface

def main(query_resolver: QueryResolverInterface):
    print(f'OnTime service running')
    query_resolver.resolve_user_query('am i free for lunch next Sunday?')

if __name__ == "__main__":
    queryResolver = get_query_resolver()
    main(queryResolver)