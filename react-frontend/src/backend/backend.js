import config from '../config/config.json'

export const TENANT_LIST = 'tenant_list'
export const EXECUTION_OPTIONS = 'execution_options'
export const GLOBAL_SETTINGS = 'global_settings'
export const ENTITY_FILTER = 'entity_filter'

export const EXTRACT_CONFIG_V2 = 'extract_config_v2'
export const EXTRACT_ENTITY_V2 = 'extract_entity_v2'

export const MATCH_ENTITIES_V2 = 'match_entities_v2'

export const MIGRATE_CONFIG_V2 = 'migrate_config_v2'


export function backendGet(api_method, searchParams, thenFunction) {

    const requestOptions = {
        method: 'GET',
        mode: 'cors',
    };

    return fetchRunThen(api_method, requestOptions, searchParams, thenFunction)
}

export function backendPost(api_method, payload, searchParams, thenFunction) {

    const requestOptions = {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        mode: 'cors',
        body: JSON.stringify(payload)
    };

    return fetchRunThen(api_method, requestOptions, searchParams, thenFunction)
}

export function backendDelete(api_method, payload, searchParams, thenFunction) {

    const requestOptions = {
        method: 'DELETE',
        headers: { 'Content-Type': 'application/json' },
        mode: 'cors',
        body: JSON.stringify(payload)
    };

    return fetchRunThen(api_method, requestOptions, searchParams, thenFunction)
}

function fetchRunThen(api_method, requestOptions, searchParams, thenFunction) {
    const fetchPromise = buildFetch(api_method, requestOptions, searchParams)

    if (thenFunction instanceof Function) {
        const validationPromise = validateReturnCodePromise(fetchPromise, api_method, thenFunction)

        console.log(validationPromise)

        return validationPromise
            .catch((error) => {
                alert("Error Backend Api: " + api_method + "\n" + error)
            })
    }

    alert("DEV ERROR: thenFunction not a function", thenFunction)
    console.trace()
}

function validateReturnCodePromise(fetchPromise, api_method, thenFunction) {
    return fetchPromise.then(response => {
        if (response.ok) {
            return thenFunction(Promise.resolve(response))
        } else if (response.status >= 400) {

            const throwHTTPError = (responseTextPromise) => {
                responseTextPromise.then(responseText => {
                    console.log(responseText)
                    throw new Error("Http Status: " + response.status + "\nBody: " + responseText)
                })
                .catch((error) => {
                    alert("Error Backend Api: " + api_method + "\n" + error)
                })

            }

            return throwHTTPError(response.text())
        }
    })
}

function buildFetch(api_method, requestOptions, searchParams) {
    return fetch(getBackendURL(api_method, searchParams), requestOptions)
}

function getBackendURL(api_method, searchParams) {
    let searchParamsString = ""

    if (searchParams) {
        searchParamsString += '?' + new URLSearchParams(searchParams)
    }

    return 'http://' + config.backend_host + '/' + api_method + searchParamsString
}