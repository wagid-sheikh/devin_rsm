/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CompanyCreate } from '../models/CompanyCreate';
import type { CompanyResponse } from '../models/CompanyResponse';
import type { CompanyUpdate } from '../models/CompanyUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CompaniesService {
    /**
     * List Companies
     * @returns CompanyResponse Successful Response
     * @throws ApiError
     */
    public static listCompaniesApiV1CompaniesGet(): CancelablePromise<Array<CompanyResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/companies',
        });
    }
    /**
     * Create Company
     * @param requestBody
     * @returns CompanyResponse Successful Response
     * @throws ApiError
     */
    public static createCompanyApiV1CompaniesPost(
        requestBody: CompanyCreate,
    ): CancelablePromise<CompanyResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/companies',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Company
     * @param companyId
     * @returns CompanyResponse Successful Response
     * @throws ApiError
     */
    public static getCompanyApiV1CompaniesCompanyIdGet(
        companyId: number,
    ): CancelablePromise<CompanyResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/companies/{company_id}',
            path: {
                'company_id': companyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Company
     * @param companyId
     * @param requestBody
     * @returns CompanyResponse Successful Response
     * @throws ApiError
     */
    public static updateCompanyApiV1CompaniesCompanyIdPatch(
        companyId: number,
        requestBody: CompanyUpdate,
    ): CancelablePromise<CompanyResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/companies/{company_id}',
            path: {
                'company_id': companyId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Company
     * @param companyId
     * @returns void
     * @throws ApiError
     */
    public static deleteCompanyApiV1CompaniesCompanyIdDelete(
        companyId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/companies/{company_id}',
            path: {
                'company_id': companyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
