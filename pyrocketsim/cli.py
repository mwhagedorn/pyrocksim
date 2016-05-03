import click
from repository import Repository
from simulation import Simulation

@click.group(name='pyrocksim')
@click.pass_context
def cli(ctx):
    """
    Outputs messages.
    """
    ctx.obj = Repository()


@cli.command(name="run")
@click.argument('rocket')
@click.argument('engine')
@click.pass_context
def run(ctx,rocket,engine):
    """
    Executes the sim with [rockets, engine]
    """
    rocket = ctx.obj.find_rocket_by_name(rocket)
    assert rocket is not None
    engine = ctx.obj.find_engine_by_code(engine)
    assert engine is not None

    return Simulation(rocket,engine).execute()



@cli.group(name="create")
@click.pass_context
def create(ctx):
    """
    Create [rocket]
    """

@create.command()
@click.argument('name')
@click.argument('empty_weight')
@click.argument('diameter')
@click.argument('drag_coefficient')
@click.pass_context
def rocket(ctx, name, empty_weight, diameter, drag_coefficient):
    """
    Create Rocket in the repository
    :param name: rocket name
    :param empty_weight: weight in grams
    :param diameter: diameter in mm
    :param drag_coefficient: the drag coefficient.  start with 0.8
    :return:
    """
    pass


@cli.group(name="list")
@click.pass_context
def list(ctx):
    """
    Lists the [rockets, engines]
    """

@list.command()
@click.pass_context
def rockets(ctx):
    """
    Lists the rockets in the repository
    """
    click.echo("List rockets")
    print(ctx.obj.all_rockets())


@list.command()
@click.pass_context
def engines(ctx):
    """
    Lists the engines in the repository
    """
    click.echo("List engines")
    print(ctx.obj.all_engines())

@cli.group()
@click.pass_context
def show(ctx):
    """
    Show the specifics on an entity
    """

@show.command()
@click.argument('name')
@click.pass_context
def rocket(ctx,name):
    """
    Show details on a specific rocket
    """
    click.echo("List rockets by name")
    print(ctx.obj.find_rocket_by_name(name))


@show.command()
@click.argument('name')
@click.pass_context
def engine(ctx,name):
    """
    Show details on a specific engine
    """
    click.echo("List engine {0}".format(name))

@show.command()
@click.pass_context
def repository(ctx):
    """
    Show details of the repository
    """
    click.echo("Show repository")
    click.echo(ctx.obj)




if __name__ == '__main__':
    cli()



