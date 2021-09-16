from plotnine import ggplot, geom_point, aes, geom_line, scale_x_continuous, scale_fill_manual
import pygal


def elbow(df, test_ks):
    '''
    ggplot to identify elbow in k means clustering inertia graph
    '''
    return (ggplot(df, aes(x='ks', y='ssod'))
            + geom_point()
            + geom_line()
            + scale_x_continuous(breaks=test_ks))


def cluster(df):
    '''
    ggplot to show clusters from k means 
    '''
    return(ggplot(df, aes(x='x', y='y', color='cluster'))
           + geom_point()
           + scale_fill_manual(values='cols', breaks='cluster')
           )

def bar_graph(series, title):
    '''
    pygal generates an svg object to pass to template
    '''
    bar = pygal.Bar(title=title)
    for k, v in series.iteritems():
        print(type(k), type(v))
        bar.add(k, v)
    return bar.render_data_uri()


def pie_chart(series, title):
    '''
    pygal generates an svg object to pass to template
    '''
    pie = pygal.Pie(title=title)
    for k, v in series.iteritems():
        pie.add(k, v)
    return pie.render_data_uri()
