/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CompanyCostCenterCreate } from '../models/CompanyCostCenterCreate';
import type { CompanyCostCenterResponse } from '../models/CompanyCostCenterResponse';
import type { CostCenterCreate } from '../models/CostCenterCreate';
import type { CostCenterResponse } from '../models/CostCenterResponse';
import type { CostCenterUpdate } from '../models/CostCenterUpdate';
import type { CancelablePromise } from '../core/CancelablePromise';
import { OpenAPI } from '../core/OpenAPI';
import { request as __request } from '../core/request';
export class CostCentersService {
    /**
     * Create Cost Center
     * Create a new global cost center (PLATFORM_ADMIN only).
     * @param requestBody
     * @returns CostCenterResponse Successful Response
     * @throws ApiError
     */
    public static createCostCenterApiV1CostCentersPost(
        requestBody: CostCenterCreate,
    ): CancelablePromise<CostCenterResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/cost-centers',
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Cost Centers
     * List all global cost centers.
     * @param activeOnly
     * @returns CostCenterResponse Successful Response
     * @throws ApiError
     */
    public static listCostCentersApiV1CostCentersGet(
        activeOnly: boolean = true,
    ): CancelablePromise<Array<CostCenterResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/cost-centers',
            query: {
                'active_only': activeOnly,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Get Cost Center
     * Get a specific cost center by ID.
     * @param costCenterId
     * @returns CostCenterResponse Successful Response
     * @throws ApiError
     */
    public static getCostCenterApiV1CostCentersCostCenterIdGet(
        costCenterId: number,
    ): CancelablePromise<CostCenterResponse> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/cost-centers/{cost_center_id}',
            path: {
                'cost_center_id': costCenterId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Update Cost Center
     * Update a cost center (PLATFORM_ADMIN only).
     * @param costCenterId
     * @param requestBody
     * @returns CostCenterResponse Successful Response
     * @throws ApiError
     */
    public static updateCostCenterApiV1CostCentersCostCenterIdPatch(
        costCenterId: number,
        requestBody: CostCenterUpdate,
    ): CancelablePromise<CostCenterResponse> {
        return __request(OpenAPI, {
            method: 'PATCH',
            url: '/api/v1/cost-centers/{cost_center_id}',
            path: {
                'cost_center_id': costCenterId,
            },
            body: requestBody,
            mediaType: 'application/json',
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Delete Cost Center
     * Soft delete a cost center (PLATFORM_ADMIN only).
     * @param costCenterId
     * @returns void
     * @throws ApiError
     */
    public static deleteCostCenterApiV1CostCentersCostCenterIdDelete(
        costCenterId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/cost-centers/{cost_center_id}',
            path: {
                'cost_center_id': costCenterId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * List Company Cost Centers
     * List cost centers assigned to a company.
     * @param companyId
     * @returns CompanyCostCenterResponse Successful Response
     * @throws ApiError
     */
    public static listCompanyCostCentersApiV1CostCentersCompaniesCompanyIdCostCentersGet(
        companyId: number,
    ): CancelablePromise<Array<CompanyCostCenterResponse>> {
        return __request(OpenAPI, {
            method: 'GET',
            url: '/api/v1/cost-centers/companies/{company_id}/cost-centers',
            path: {
                'company_id': companyId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
    /**
     * Assign Cost Center To Company
     * Assign a cost center to a company.
     * @param companyId
     * @param requestBody
     * @returns CompanyCostCenterResponse Successful Response
     * @throws ApiError
     */
    public static assignCostCenterToCompanyApiV1CostCentersCompaniesCompanyIdCostCentersPost(
        companyId: number,
        requestBody: CompanyCostCenterCreate,
    ): CancelablePromise<CompanyCostCenterResponse> {
        return __request(OpenAPI, {
            method: 'POST',
            url: '/api/v1/cost-centers/companies/{company_id}/cost-centers',
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
     * Remove Cost Center From Company
     * Remove a cost center assignment from a company.
     * @param companyId
     * @param assignmentId
     * @returns void
     * @throws ApiError
     */
    public static removeCostCenterFromCompanyApiV1CostCentersCompaniesCompanyIdCostCentersAssignmentIdDelete(
        companyId: number,
        assignmentId: number,
    ): CancelablePromise<void> {
        return __request(OpenAPI, {
            method: 'DELETE',
            url: '/api/v1/cost-centers/companies/{company_id}/cost-centers/{assignment_id}',
            path: {
                'company_id': companyId,
                'assignment_id': assignmentId,
            },
            errors: {
                422: `Validation Error`,
            },
        });
    }
}
