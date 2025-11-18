/**
 * TypeScript type definitions for AWS Incident Co-Pilot
 */

export type IncidentSeverity = 'LOW' | 'MEDIUM' | 'HIGH' | 'CRITICAL';

export interface Incident {
  id: string;
  title: string;
  severity: IncidentSeverity;
  resource: string;
  description: string;
  detected_at: string;
  recommendations?: string[];
  cost_impact?: string;
}

export interface CostInfo {
  estimated_cost_per_scan?: string;
  free_tier_eligible?: boolean;
  aws_services_used?: string[];
  recommendation?: string;
  note?: string;
  endpoint_cost?: string;
  vercel_cost?: string;
  test_cost?: string;
  free_tier?: string;
}

export interface ScanResponse {
  success: boolean;
  incidents: Incident[];
  incident_count?: number;
  region?: string;
  scanned_at?: string;
  cost_info?: CostInfo;
  error?: string;
  demo_mode?: boolean;
  warning?: string;
  help?: string | { message: string; required_env_vars: string[]; setup_guide: string };
  troubleshooting?: Record<string, string>;
  support?: string;
}

export interface AWSTestResponse {
  configured: boolean;
  has_access_key: boolean;
  has_secret_key: boolean;
  region: string;
  connected?: boolean;
  account_id?: string;
  user_arn?: string;
  user_id?: string;
  permissions?: Record<string, string>;
  all_permissions_ok?: boolean;
  cost_info?: CostInfo;
  error?: string;
  error_code?: string;
  warning?: string;
  recommendation?: string;
  help?: string | { message: string; required_env_vars: string[]; setup_guide: string };
}

export interface APIError {
  message: string;
  code?: string;
  details?: string;
}
