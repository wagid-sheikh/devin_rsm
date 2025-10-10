/* generated using openapi-typescript-codegen -- do not edit */
/* istanbul ignore file */
/* tslint:disable */
/* eslint-disable */
export type UserStoreAccessCreate = {
    store_id: number;
    scope?: UserStoreAccessCreate.scope;
};
export namespace UserStoreAccessCreate {
    export enum scope {
        VIEW = 'view',
        EDIT = 'edit',
        APPROVE = 'approve',
    }
}

