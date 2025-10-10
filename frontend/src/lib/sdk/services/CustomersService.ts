/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustomerCreate } from '../models/CustomerCreate';
import type { CustomerResponse } from '../models/CustomerResponse';
import type { CustomerUpdate } from '../models/CustomerUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CustomersService {
    /**
     * Create Customer
     * Create a new customer.
     * @param requestBody
     * @returns CustomerResponse Successful Response
     * @throws ApiError
     */
    public static createCustomerApiV1CustomersPost(
        requestBody: CustomerCreate,
    ): CancelablePromise<CustomerResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/customers',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Customers
     * List all customers for the user's company with optional search.
     * @param search Search by name, phone, or email
     * @param statusFilter Filter by status (active/inactive)
     * @returns CustomerResponse Successful Response
     * @throws ApiError
     */
    public static listCustomersApiV1CustomersGet(
        search?: (string | null),
        statusFilter?: (string | null),
    ): CancelablePromise<Array<CustomerResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/customers',
            query: {
                'search': search,
                'status_filter': statusFilter,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Customer
     * Get a specific customer by ID.
     * @param customerId
     * @returns CustomerResponse Successful Response
     * @throws ApiError
     */
    public static getCustomerApiV1CustomersCustomerIdGet(
        customerId: number,
    ): CancelablePromise<CustomerResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/customers/{customer_id}',
            path: {
                'customer_id': customerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Customer
     * Update a customer.
     * @param customerId
     * @param requestBody
     * @returns CustomerResponse Successful Response
     * @throws ApiError
     */
    public static updateCustomerApiV1CustomersCustomerIdPatch(
        customerId: number,
        requestBody: CustomerUpdate,
    ): CancelablePromise<CustomerResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/customers/{customer_id}',
            path: {
                'customer_id': customerId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Customer
     * Soft delete a customer by setting status to inactive.
     * @param customerId
     * @returns void
     * @throws ApiError
     */
    public static deleteCustomerApiV1CustomersCustomerIdDelete(
        customerId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/customers/{customer_id}',
            path: {
                'customer_id': customerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
