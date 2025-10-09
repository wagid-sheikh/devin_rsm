/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
import type { RoleResponse } from './RoleResponse';
export type UserResponse = {
    id: number;
    email: string;
    phone: (string | null);
    first_name: string;
    last_name: string;
    status: string;
    roles: Array<RoleResponse>;
    created_at: string;
    updated_at: string;
};

