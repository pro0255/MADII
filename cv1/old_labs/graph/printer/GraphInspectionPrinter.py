
from old_labs.graph.GraphProperties import GRAPH_PROPERTIES, GRAPH_CONNECTED_COMPONENTS_PROPERTIES, GRAPH_INSPECTION

DELIMITER = '=============================================================='

properties_translation = {
    GRAPH_PROPERTIES.GRAPH_AVERAGE: 'Prumer grafu',
    GRAPH_PROPERTIES.AVERAGE_DISTANCE: 'Prumerna vzdalenost v grafu',
    GRAPH_PROPERTIES.MAX_DEGREE: 'Maximalni stupen v grafu',
    GRAPH_PROPERTIES.MIN_DEGREE: 'Minimalni stupen v grafu',
    GRAPH_PROPERTIES.AVG_DEGREE: 'Prumerny stupen v grafu',
    GRAPH_PROPERTIES.DEGREE_DISTRIBUTION: 'Distribuce stupnu v grafu',
    GRAPH_PROPERTIES.FLOYD_MATRIX:'Floyd matice',
    GRAPH_PROPERTIES.ADJECENCY_MATRIX: 'Matice sousednosti',
    GRAPH_PROPERTIES.GRAPH_TRANSITIVITY: 'Tranzitivita v grafu',
    GRAPH_PROPERTIES.CLOSSNES_CENTRALITY: 'Closness centralita',
    GRAPH_PROPERTIES.CLUSTER_COEFFICIENT: 'Shlukovaci koeficient',
}

connected_components_properties_translations = {
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.NUMBER_OF_CONNECTED_COMPONENTS: 'Pocet komponent souvislosti',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.MAX_CONNECTED_COMPONENT: 'Nejvetsi velikost v ramci komponent souvislosti',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.MIN_CONNECTED_COMPONENT: 'Nejmensi velikost v ramci komponent souvislosti',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS: 'Komponenty',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_PROPERTIES: 'Vlastnosti komponent',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_SIZES: 'Velikosti komponent souvislosti',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER: 'Rozlozeni komponent souvislosti',
    GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_GRAPH_AVERAGE_OVER_ALL: 'Prumer grafu pres jednoltive komponenty souvilosti'
}


def create_string_for_graph_properties(properties):
    output = ""

    output += f'{properties_translation[GRAPH_PROPERTIES.GRAPH_AVERAGE]} je {properties[GRAPH_PROPERTIES.GRAPH_AVERAGE]}\n'
    output += f'{properties_translation[GRAPH_PROPERTIES.AVERAGE_DISTANCE]} je {properties[GRAPH_PROPERTIES.AVERAGE_DISTANCE]}\n'
    output += f'{properties_translation[GRAPH_PROPERTIES.MAX_DEGREE]} je {properties[GRAPH_PROPERTIES.MAX_DEGREE]}\n'
    output += f'{properties_translation[GRAPH_PROPERTIES.MIN_DEGREE]} je {properties[GRAPH_PROPERTIES.MIN_DEGREE]}\n'
    output += f'{properties_translation[GRAPH_PROPERTIES.AVG_DEGREE]} je {properties[GRAPH_PROPERTIES.AVG_DEGREE]}\n'

    output += f'{properties_translation[GRAPH_PROPERTIES.DEGREE_DISTRIBUTION]} je:\n'
    for k,v in sorted(properties[GRAPH_PROPERTIES.DEGREE_DISTRIBUTION].items()):
        output += f'\tStupen {k} je obsazen {v} krat, s relativni cetnosti {v/sum(properties[GRAPH_PROPERTIES.DEGREE_DISTRIBUTION].values())}\n'

    output += f'{properties_translation[GRAPH_PROPERTIES.CLOSSNES_CENTRALITY]} je:\n'
    for index, value in enumerate(properties[GRAPH_PROPERTIES.CLOSSNES_CENTRALITY]):
        output += f'\tUzel {index} hodnota {value}\n'

    output += f'{properties_translation[GRAPH_PROPERTIES.CLUSTER_COEFFICIENT]} je:\n'
    for index, value in enumerate(properties[GRAPH_PROPERTIES.CLUSTER_COEFFICIENT]):
        output += f'\tUzel {index} hodnota {value}\n'

    output += f'{properties_translation[GRAPH_PROPERTIES.GRAPH_TRANSITIVITY]} je {properties[GRAPH_PROPERTIES.GRAPH_TRANSITIVITY]}\n'

    return output


def create_string_for_graph_properties_for_connected_components(connected_components):
    output = ""

    output += f'{connected_components_properties_translations[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.NUMBER_OF_CONNECTED_COMPONENTS]} je {connected_components["number_of_connected_components"]}\n'
    output += f'{connected_components_properties_translations[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.MAX_CONNECTED_COMPONENT]} je {connected_components["max_connected_component"]}\n'

    output += f'{connected_components_properties_translations[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.MIN_CONNECTED_COMPONENT]} je {connected_components["min_connected_component"]}\n'

    output += f'{connected_components_properties_translations[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_GRAPH_AVERAGE_OVER_ALL]} je {connected_components["graph_average_over_all"]}\n'



    output += f'{connected_components_properties_translations[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER]} je \n'
    for k,v in sorted(connected_components[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER].items()):
        output += f'\tKomponent s velikosti {k} je {v}, relativni cetnost {v/sum(connected_components[GRAPH_CONNECTED_COMPONENTS_PROPERTIES.COMPONENTS_COUNTER].values())}\n'

    
    com_props = connected_components["components_properties"]

    for index ,component_dic in enumerate(com_props):
        component_output = create_string_for_graph_properties(component_dic)
        output += f'{DELIMITER}\n{index}\n{DELIMITER}\n{component_output}'


    return output


def create_graph_inspections_string(graph_inspection):
    output = ""
    whole_properties = graph_inspection[GRAPH_INSPECTION.WHOLE]
    connected_components_properties = graph_inspection[GRAPH_INSPECTION.CONNECTED_COMPONENTS]
    output += f'CELY GRAF \n{create_string_for_graph_properties(whole_properties)}\n{DELIMITER}\n'
    output += f'KOMPONENTY SOUVILOSTI \n{create_string_for_graph_properties_for_connected_components(connected_components_properties)}\n{DELIMITER}\n'
    return output


def print_graph_inspection(graph_inspection):
    print(create_graph_inspections_string(graph_inspection))


def write_graph_inspection_to_file(path, graph_inspection, des=""):
    final = f'{des} \n\n\n {create_graph_inspections_string(graph_inspection)}'
    with open(path, 'w') as f:
        f.write(final)    