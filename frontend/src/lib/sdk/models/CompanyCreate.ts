/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CompanyAddress } from './CompanyAddress';
import type { CompanyContacts } from './CompanyContacts';
import type { CompanyGSTINCreate } from './CompanyGSTINCreate';
export type CompanyCreate = {
    legal_name: string;
    trade_name?: (string | null);
    pan?: (string | null);
    contacts: CompanyContacts;
    address: CompanyAddress;
    gstins?: Array<CompanyGSTINCreate>;
};

