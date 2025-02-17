
import api_v2
import handler_api


def extract_schemas(config, use_cache=True, cache_only=False):
    schema_dict = handler_api.extract_basic_json(
        config, api_v2.settings_schemas, 'settings_schemas',
        use_cache, cache_only)

    return schema_dict


def extract_function(config, use_cache, cache_only, analysis_object, input_params=None):

    schema_dict = extract_schemas(
        config, use_cache=False, cache_only=cache_only)

    _ = extract_configs(
        item_id_query_dict_extractor, config, schema_dict, use_cache, cache_only, analysis_object)

    return schema_dict


def extract_specific_scope(config, use_cache, cache_only, analysis_object, scope):

    scope_dict = {"items": [{"scope": scope}]}

    _ = extract_configs(
        scope_query_dict_extractor, config, scope_dict, use_cache, cache_only, analysis_object)

    return scope_dict


def extract_configs(item_id_extractor, config, input_dict, use_cache, cache_only, analysis_object=None):

    handler_api.extract_pages_from_input_list(
        config, input_dict['items'],
        'objects', api_v2.settings_objects, item_id_extractor,
        use_cache, cache_only, analysis_object)

    return None


def item_id_query_dict_extractor(item):

    item_id = item['schemaId']

    query_dict = {}
    query_dict['schemaIds'] = item_id
    query_dict['fields'] = "objectId,scope,schemaId,value"

    return item_id, query_dict


def scope_query_dict_extractor(item):

    scope = item['scope']

    query_dict = {}
    query_dict['scopes'] = scope
    query_dict['fields'] = "objectId,scope,schemaId,value"

    return scope, query_dict
