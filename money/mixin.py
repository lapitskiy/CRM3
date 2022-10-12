class CacheQuerysetMixin:
    '''
    A mixin that caches the list of records obtained via mptt.get_cached_trees
    into the _cached_queryset attribute.
    Otherwise two identical queries will be executed
    Supported depth attribute which specifies the length of mptt descendants
    '''

    _cached_queryset = None

    def _caching_queryset(self, queryset=None):
        if not self._cached_queryset:
            print('NOT CACHED ', self._cached_queryset)
            print('QUERY ', queryset)
            self._cached_queryset = queryset
        return self._cached_queryset

    def _check_cached(self):
        if not self._cached_queryset:
            return False
        return True

    def _get_cached_queryset(self):
        return self._cached_queryset



