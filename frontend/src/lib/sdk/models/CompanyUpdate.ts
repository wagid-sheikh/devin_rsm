/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { CompanyAddress } from './CompanyAddress';
import type { CompanyContacts } from './CompanyContacts';
export type CompanyUpdate = {
    legal_name?: (string | null);
    trade_name?: (string | null);
    pan?: (string | null);
    contacts?: (CompanyContacts | null);
    address?: (CompanyAddress | null);
    status?: (string | null);
};

