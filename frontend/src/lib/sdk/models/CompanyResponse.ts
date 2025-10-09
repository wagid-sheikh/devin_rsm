/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CompanyAddress } from './CompanyAddress';
import type { CompanyContacts } from './CompanyContacts';
import type { CompanyGSTINResponse } from './CompanyGSTINResponse';
export type CompanyResponse = {
    id: number;
    legal_name: string;
    trade_name: (string | null);
    pan: (string | null);
    contacts: CompanyContacts;
    address: CompanyAddress;
    status: string;
    gstins: Array<CompanyGSTINResponse>;
    created_at: string;
    updated_at: string;
};

