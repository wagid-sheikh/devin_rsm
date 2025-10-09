/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CompanyAddress = {
    address_line1: string;
    address_line2?: (string | null);
    city: string;
    /**
     * Indian state name
     */
    state: string;
    /**
     * 6-digit Indian postal code
     */
    pincode: string;
    country?: string;
    landmark?: (string | null);
};

