import os
import click
import pandas as pd
import jinja2



@click.command()
@click.argument('input_file', type=click.File(mode='r', lazy=True))
@click.argument('template_file', type=click.File(mode='r', lazy=True))
@click.argument('output_path', type=click.Path(exists=True, writable=True), default=lambda: os.getcwd())
@click.option('--output_filename', help='Jinja2 template string to generate filenames')
@click.option('--delimiter', default=',')
def cli(input_file, output_path, template_file, output_filename, delimiter):
    template_extension = os.path.splitext(template_file.name)[-1]
    template = jinja2.Template(template_file.read())
    click.echo('Opening file %s for parsing' % input_file.name)
    data = pd.read_csv(input_file, parse_dates=True, delimiter=delimiter, skipinitialspace=True)
    for row in data.itertuples():
        values = row._asdict()
        if not output_filename:
            filename = str(row.Index) + template_extension
        else:
            filename = jinja2.Environment().from_string(output_filename).render(**values)
        click.echo('Writing to %s' % os.path.join(output_path, filename))
        with open(os.path.join(output_path, filename), mode='w') as output_file:
            output_file.write(template.render(**values))
            output_file.flush()


if __name__ == '__main__':
    cli()  # pylint: disable=no-value-for-parameter
