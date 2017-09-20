from jinja2 import Environment, PackageLoader, StrictUndefined

env = Environment(
    loader=PackageLoader('mapboxgl', 'templates'),
    autoescape=False,
    undefined=StrictUndefined
)


def format(viz, **kwargs):
    template = env.get_template('{}.html'.format(viz))
    return template.render(viz=viz, **kwargs)
