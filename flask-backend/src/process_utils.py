from flask import request
import json
import handler_api
from filter import AnalysisFilter

UNIQUE_ENTITY_LIST = ['environment']


def execute_match(run_info, analysis_class, analysis_filter,
                  extract_function, live_extract=False):

    all_tenant_match_dict = {}

    for tenant_dict in run_info['tenant_dict_list']:

        tenant_key = tenant_dict['tenant_key']

        if(tenant_key in all_tenant_match_dict):
            pass
        else:

            if(live_extract):
                handler_api.pull(tenant_key, extract_function,
                                 use_cache=False, input_params=tenant_dict['scope'])

            analysis_filter.set_time_filter_type(
                tenant_dict['is_target_tenant'])
            analysis_object = analysis_class(analysis_filter)

            all_tenant_match_dict[tenant_key] = handler_api.analyze(
                tenant_key, extract_function, analysis_object, input_params=tenant_dict['scope'])

    return run_info, all_tenant_match_dict


def get_run_info(tenant_key_main, tenant_key_target, context_params=None, entity_filter=None):
    run_info = {}

    run_info = set_run_tags(
        tenant_key_main, tenant_key_target, context_params, run_info)
    run_info['tenant_dict_list'] = get_tenant_dict_list(
        tenant_key_main, tenant_key_target, run_info, context_params)
    run_info['tenant_key_main'] = tenant_key_main
    run_info['tenant_key_target'] = tenant_key_target
    run_info = set_analysis_filter(run_info, entity_filter)

    return run_info


def set_analysis_filter(run_info, entity_filter):
    if(run_info['unique_entity']):
        entity_filter = UNIQUE_ENTITY_LIST
    
    run_info['analysis_filter'] = AnalysisFilter(entity_filter)
    
    return run_info

def set_run_tags(tenant_key_main, tenant_key_target, context_params, run_info):
    run_info['self_match'] = (tenant_key_main == tenant_key_target)
    run_info['forced_match'] = (context_params is not None
                                and 'provided_id' in context_params)
    run_info['unique_entity'] = False

    if(run_info['forced_match']):
        for target, main in context_params['provided_id'].items():
            if(target in UNIQUE_ENTITY_LIST
               or main in UNIQUE_ENTITY_LIST):
                run_info['unique_entity'] = True
                
    return run_info


def get_tenant_dict_list(tenant_key_main, tenant_key_target, run_info, context_params=None):

    tenant_dict_list = []

    scope_main = None
    scope_target = None

    if(context_params is None):
        pass
    else:
        if(run_info['forced_match']):

            for target, main in context_params['provided_id'].items():
                scope_main = main
                scope_target = target

    tenant_dict_list.append(create_tenant_dict(
        tenant_key_main, False, scope_main))
    tenant_dict_list.append(create_tenant_dict(
        tenant_key_target, True, scope_target))

    return tenant_dict_list


def create_tenant_dict(tenant_key, is_target_tenant, scope):
    return {'tenant_key': tenant_key, 'is_target_tenant': is_target_tenant, 'scope': scope}


def get_arg_json(key, default=None):
    value = request.args.get(key)

    if(value is None):
        return default

    return json.loads(value)


def get_arg_bool(key, default=None):
    value = get_arg(key, default=None)
    valid = False

    if(isinstance(value, str)):
        if((value.lower()) == "false"):
            value = False
            valid = True
        elif((value.lower()) == "true"):
            value = True
            valid = True

    if(valid == False):
        print("Bad parameter value for", key, value, "using default:", default)
        return default

    return value


def get_arg_int(key, default=None):
    value = get_arg(key, default=None)
    valid = False

    if(value is None):
        pass
    elif(value.isnumeric()
         and float(value).is_integer()):
        value = int(value)
        valid = True

    if(value == True):
        print("Bad parameter value for", key, value, "using default:", default)
        value = default

    return value
