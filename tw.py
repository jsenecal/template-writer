import os
import sys
import logging
import click
import pandas as pd
import jinja2

logger = logging.getLogger()


@click.command()
@click.argument('input_file', type=click.File(mode='r'))
@click.argument('template_file', type=click.File(mode='r', lazy=True))
@click.argument('output_path', type=click.Path(exists=True, writable=True), default=lambda: os.getcwd())
@click.option('--output_filename')
@click.option('--delimiter', default=',')
def cli(input_file, output_path, template_file, output_filename, delimiter):
    searchpath = os.path.dirname(template_file.name)
    file_extension = os.path.splitext(template_file.name)[-1]

    env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(searchpath=searchpath),
        autoescape=jinja2.select_autoescape(['xml'])
    )

    template = env.get_template(template_file.name)
    data = pd.read_csv(input_file, parse_dates=True, delimiter=delimiter)
    for row in data.itertuples():
        values = row._asdict()
        if not output_filename:
            filename = str(row.Index) + file_extension
        else:
            filename = jinja2.Environment().from_string(output_filename).render(**values)
        output_file = open(output_path + filename, mode='w')
        output_file.write(template.render(**values))


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
