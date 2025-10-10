/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CustomerAddressResponse } from './CustomerAddressResponse';
import type { CustomerContactResponse } from './CustomerContactResponse';
export type CustomerResponse = {
    id: number;
    company_id: number;
    code: (string | null);
    name: string;
    phone_primary: string;
    email: (string | null);
    notes: (string | null);
    status: string;
    contacts: Array<CustomerContactResponse>;
    addresses: Array<CustomerAddressResponse>;
    created_at: string;
    updated_at: string;
};

