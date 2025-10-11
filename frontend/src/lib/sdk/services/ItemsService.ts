/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { ItemCreate } from '../models/ItemCreate';
import type { ItemResponse } from '../models/ItemResponse';
import type { ItemUpdate } from '../models/ItemUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class ItemsService {
    /**
     * Create Item
     * @param requestBody
     * @returns ItemResponse Successful Response
     * @throws ApiError
     */
    public static createItemApiV1ItemsPost(
        requestBody: ItemCreate,
    ): CancelablePromise<ItemResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/items',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Items
     * @param search Search by SKU or name
     * @param statusFilter Filter by status (active/inactive)
     * @param typeFilter Filter by type (service/product)
     * @returns ItemResponse Successful Response
     * @throws ApiError
     */
    public static listItemsApiV1ItemsGet(
        search?: (string | null),
        statusFilter?: (string | null),
        typeFilter?: (string | null),
    ): CancelablePromise<Array<ItemResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/items',
            query: {
                'search': search,
                'status_filter': statusFilter,
                'type_filter': typeFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Item
     * @param itemId
     * @returns ItemResponse Successful Response
     * @throws ApiError
     */
    public static getItemApiV1ItemsItemIdGet(
        itemId: number,
    ): CancelablePromise<ItemResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/items/{item_id}',
            path: {
                'item_id': itemId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Item
     * @param itemId
     * @param requestBody
     * @returns ItemResponse Successful Response
     * @throws ApiError
     */
    public static updateItemApiV1ItemsItemIdPatch(
        itemId: number,
        requestBody: ItemUpdate,
    ): CancelablePromise<ItemResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/items/{item_id}',
            path: {
                'item_id': itemId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
