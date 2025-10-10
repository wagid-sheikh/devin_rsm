/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CustomerCreate = {
    code?: (string | null);
    name: string;
    /**
     * Phone number in E.164 format
     */
    phone_primary: string;
    email?: (string | null);
    notes?: (string | null);
};

