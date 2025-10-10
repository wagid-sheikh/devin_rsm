/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustomerAddressCreate } from '../models/CustomerAddressCreate';
import type { CustomerAddressResponse } from '../models/CustomerAddressResponse';
import type { CustomerAddressUpdate } from '../models/CustomerAddressUpdate';
import type { CustomerContactCreate } from '../models/CustomerContactCreate';
import type { CustomerContactResponse } from '../models/CustomerContactResponse';
import type { CustomerContactUpdate } from '../models/CustomerContactUpdate';
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
    /**
     * Create Customer Contact
     * Create a new contact for a customer.
     * @param customerId
     * @param requestBody
     * @returns CustomerContactResponse Successful Response
     * @throws ApiError
     */
    public static createCustomerContactApiV1CustomersCustomerIdContactsPost(
        customerId: number,
        requestBody: CustomerContactCreate,
    ): CancelablePromise<CustomerContactResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/customers/{customer_id}/contacts',
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
     * List Customer Contacts
     * List all contacts for a customer.
     * @param customerId
     * @returns CustomerContactResponse Successful Response
     * @throws ApiError
     */
    public static listCustomerContactsApiV1CustomersCustomerIdContactsGet(
        customerId: number,
    ): CancelablePromise<Array<CustomerContactResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/customers/{customer_id}/contacts',
            path: {
                'customer_id': customerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Customer Contact
     * Update a customer contact.
     * @param customerId
     * @param contactId
     * @param requestBody
     * @returns CustomerContactResponse Successful Response
     * @throws ApiError
     */
    public static updateCustomerContactApiV1CustomersCustomerIdContactsContactIdPatch(
        customerId: number,
        contactId: number,
        requestBody: CustomerContactUpdate,
    ): CancelablePromise<CustomerContactResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/customers/{customer_id}/contacts/{contact_id}',
            path: {
                'customer_id': customerId,
                'contact_id': contactId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Customer Contact
     * Delete a customer contact.
     * @param customerId
     * @param contactId
     * @returns void
     * @throws ApiError
     */
    public static deleteCustomerContactApiV1CustomersCustomerIdContactsContactIdDelete(
        customerId: number,
        contactId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/customers/{customer_id}/contacts/{contact_id}',
            path: {
                'customer_id': customerId,
                'contact_id': contactId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Create Customer Address
     * Create a new address for a customer.
     * @param customerId
     * @param requestBody
     * @returns CustomerAddressResponse Successful Response
     * @throws ApiError
     */
    public static createCustomerAddressApiV1CustomersCustomerIdAddressesPost(
        customerId: number,
        requestBody: CustomerAddressCreate,
    ): CancelablePromise<CustomerAddressResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/customers/{customer_id}/addresses',
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
     * List Customer Addresses
     * List all addresses for a customer.
     * @param customerId
     * @returns CustomerAddressResponse Successful Response
     * @throws ApiError
     */
    public static listCustomerAddressesApiV1CustomersCustomerIdAddressesGet(
        customerId: number,
    ): CancelablePromise<Array<CustomerAddressResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/customers/{customer_id}/addresses',
            path: {
                'customer_id': customerId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Customer Address
     * Update a customer address.
     * @param customerId
     * @param addressId
     * @param requestBody
     * @returns CustomerAddressResponse Successful Response
     * @throws ApiError
     */
    public static updateCustomerAddressApiV1CustomersCustomerIdAddressesAddressIdPatch(
        customerId: number,
        addressId: number,
        requestBody: CustomerAddressUpdate,
    ): CancelablePromise<CustomerAddressResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/customers/{customer_id}/addresses/{address_id}',
            path: {
                'customer_id': customerId,
                'address_id': addressId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Customer Address
     * Delete a customer address.
     * @param customerId
     * @param addressId
     * @returns void
     * @throws ApiError
     */
    public static deleteCustomerAddressApiV1CustomersCustomerIdAddressesAddressIdDelete(
        customerId: number,
        addressId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/customers/{customer_id}/addresses/{address_id}',
            path: {
                'customer_id': customerId,
                'address_id': addressId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
