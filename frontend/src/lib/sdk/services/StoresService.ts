/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { StoreCreate } from '../models/StoreCreate';
import type { StoreResponse } from '../models/StoreResponse';
import type { StoreUpdate } from '../models/StoreUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class StoresService {
    /**
     * List Stores
     * @returns StoreResponse Successful Response
     * @throws ApiError
     */
    public static listStoresApiV1StoresGet(): CancelablePromise<Array<StoreResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/stores',
        });
    }
    /**
     * Create Store
     * @param requestBody
     * @returns StoreResponse Successful Response
     * @throws ApiError
     */
    public static createStoreApiV1StoresPost(
        requestBody: StoreCreate,
    ): CancelablePromise<StoreResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/stores',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Store
     * @param storeId
     * @returns StoreResponse Successful Response
     * @throws ApiError
     */
    public static getStoreApiV1StoresStoreIdGet(
        storeId: number,
    ): CancelablePromise<StoreResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/stores/{store_id}',
            path: {
                'store_id': storeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Store
     * @param storeId
     * @param requestBody
     * @returns StoreResponse Successful Response
     * @throws ApiError
     */
    public static updateStoreApiV1StoresStoreIdPatch(
        storeId: number,
        requestBody: StoreUpdate,
    ): CancelablePromise<StoreResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/stores/{store_id}',
            path: {
                'store_id': storeId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Store
     * @param storeId
     * @returns void
     * @throws ApiError
     */
    public static deleteStoreApiV1StoresStoreIdDelete(
        storeId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/stores/{store_id}',
            path: {
                'store_id': storeId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
