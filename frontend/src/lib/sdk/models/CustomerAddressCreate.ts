/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CustomerAddressCreate = {
    /**
     * Address type (e.g., home, office)
     */
    type: string;
    /**
     * Full address text
     */
    address: string;
    is_pickup_default?: boolean;
    is_delivery_default?: boolean;
};

