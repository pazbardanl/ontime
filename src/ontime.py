from .di_config import get_query_resolver
from src.services.interfaces import QueryResolverInterface

def main(query_resolver: QueryResolverInterface):
    print(f'OnTime service running')
    query_resolver.resolve_user_query('am i free for lunch next Sunday?')
    query_resolver.resolve_user_query('can i meet for 30 minutes next Sunday at noon?')
    query_resolver.resolve_user_query('propose slots of 15 minutes next Sunday early morning till noon.')

if __name__ == "__main__":
    queryResolver = get_query_resolver()
    main(queryResolver)