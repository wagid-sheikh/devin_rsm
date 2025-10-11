/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ServiceTypeResponse } from '../models/ServiceTypeResponse';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ServiceTypesService {
    /**
     * List Service Types
     * @returns ServiceTypeResponse Successful Response
     * @throws ApiError
     */
    public static listServiceTypesApiV1ServiceTypesGet(): CancelablePromise<Array<ServiceTypeResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/service-types',
        });
    }
}
