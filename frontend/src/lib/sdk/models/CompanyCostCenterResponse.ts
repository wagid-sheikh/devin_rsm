/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CostCenterResponse } from './CostCenterResponse';
export type CompanyCostCenterResponse = {
    id: number;
    company_id: number;
    cost_center_id: number;
    is_default: boolean;
    cost_center: CostCenterResponse;
    created_at: string;
};

