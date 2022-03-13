class Breadcrumb:
    def get_breadcrumbs(path: str) -> list[str]:
        breadcrumbs: list[Crumb] = []
        crumbs: list[str] = path.split('/')

        for crumb in crumbs:
            if not breadcrumbs: 
                breadcrumbs.append(Crumb('home', True, '/'))
                continue

            breadcrumbs.append(Crumb(crumb, crumbs.index(crumb) < len(crumbs) - 1, f'{path.split(crumb)[0]}/{crumb}'.replace('//', '/')))
            
        return breadcrumbs

class Crumb:
    def __init__(self, display, enabled, path):
        self.display: str = display
        self.enabled: bool = enabled
        self.path: str = path
