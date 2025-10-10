/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type CustomerContactCreate = {
    contact_person: string;
    /**
     * Phone number in E.164 format
     */
    phone: string;
    email?: (string | null);
    is_primary?: boolean;
};

