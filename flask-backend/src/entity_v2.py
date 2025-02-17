import api_v2
import handler_api
import process_utils

def extract_function(config, use_cache, cache_only, analysis_object, context_params=None):

    _ = extract_entities_list(
        config, use_cache, cache_only, analysis_object)

    return None


def extract_specific_scope(config, use_cache, cache_only, analysis_object, scope):
    
    scope_list = [{"scope": scope}]
    
    if(scope in process_utils.UNIQUE_ENTITY_LIST):
        return None
    
    handler_api.extract_pages_from_input_list(
        config, scope_list,
        'entities_list', api_v2.entities, scope_query_dict_extractor,
        use_cache, cache_only, analysis_object)

    return None


def extract_entities_list(config, use_cache, cache_only, analysis_object=None):

    def get_entity_list_from_types(entity_type_list_dict):

        handler_api.extract_pages_from_input_list(
            config, entity_type_list_dict['types'],
            'entities_list', api_v2.entities, item_id_query_dict_extractor,
            use_cache, cache_only, analysis_object)

    def get_entity_types():

        def item_id_query_dict_extractor(item):

            item_id = None
            query_dict = {}
            query_dict['pageSize'] = '500'

            return item_id, query_dict

        use_cache_false = False
        no_analysis = None

        handler_api.extract_pages_from_input_list(
            config, None,
            'entity_types', api_v2.entity_types, item_id_query_dict_extractor,
            use_cache_false, cache_only, no_analysis, get_entity_list_from_types)

    get_entity_types()


def item_id_query_dict_extractor(item):

    item_id = item['type']

    query_dict = {}
    query_dict['entitySelector'] = 'type("' + item_id + '")'
    query_dict['pageSize'] = '1000'
    query_dict['fields'] = '+lastSeenTms,+firstSeenTms,+tags,+managementZones,+toRelationships,+fromRelationships,+icon,+properties'
    query_dict['from'] = 'now-1d'

    # query_dict['from'] = 'now-1y' #Default is now-3d

    return item_id, query_dict


def scope_query_dict_extractor(item):

    scope = item['scope']

    query_dict = {}
    query_dict['entitySelector'] = 'entityId("' + scope + '")'
    query_dict['pageSize'] = '1000'
    query_dict['fields'] = '+lastSeenTms,+firstSeenTms,+tags,+managementZones,+toRelationships,+fromRelationships,+icon,+properties'
    query_dict['from'] = 'now-1d'

    return scope, query_dict
