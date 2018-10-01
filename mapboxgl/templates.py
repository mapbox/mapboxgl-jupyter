from jinja2 import Environment, PackageLoader, StrictUndefined

env = Environment(
    loader=PackageLoader('mapboxgl', 'templates'),
    autoescape=False,
    undefined=StrictUndefined
)


def format(viz, from_string=False, template_str=None, **kwargs):
    if from_string:
        template = env.from_string(template_str)
    else:
        template = env.get_template('{}.html'.format(viz))
    return template.render(viz=viz, **kwargs)
