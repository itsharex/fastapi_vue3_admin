export interface searchDataType {
    name?: string
    date_range?: [string, string];
}

export interface tableDataType {
    id?: number;
    index?: number;
    name?: string;
    project_id?: projectSelectorType['id'];
    description?: string;

    status?: string;
    start_time?: string;
    end_time?: string;
    summary?: {
        total: number;
        pass_rate: string;
        duration: string;
        environment: string;
        details: any[];
    };
    total_count?: number;
    success_count?: number;
    fail_count?: number;
    skip_count?: number;
    error_count?: number;
    logs?: any[];
    actual_response?: any;

    project?: {
        id?: number;
        name?: string;
    };
    created_at?: string;
    updated_at?: string;
    creator?: {
        id?: number;
        name?: string;
        username?: string;
    };
}

export interface  projectSelectorType {
    id?: number;
    name?: string;
    description?: string;
}
