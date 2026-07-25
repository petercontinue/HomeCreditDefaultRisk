const API_BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type ApplicationPayload = {
  name_contract_type: "Cash loans" | "Revolving loans";
  code_gender: "F" | "M";
  flag_own_car: "N" | "Y";
  flag_own_realty: "N" | "Y";
  cnt_children: number;
  amt_income_total: number;
  amt_credit: number;
  amt_annuity: number;
  amt_goods_price: number | null;
  name_type_suite: string;
  name_income_type: string;
  name_education_type: string;
  name_family_status: string;
  name_housing_type: string;
  age_years: number;
  employment_years: number;
  own_car_age: number | null;
  occupation_type: string | null;
  cnt_fam_members: number;
  organization_type: string;
  region_rating_client: number;
  flag_email: boolean;
  flag_phone: boolean;
  flag_work_phone: boolean;
  weekday_appr_process_start: string | null;
  lang?: string;
  consent_accepted: boolean;
  privacy_notice_version: string;
};

export type PredictionResult = {
  application_id: string;
  approved: boolean;
  default_probability: number;
  risk_level: string;
  requested_amount: number;
  max_approved_amount: number | null;
  feedback: {
    summary: string;
    positives: string[];
    concerns: string[];
    suggestions: string[];
  };
  model_version: string;
  created_at?: string;
};

export type FormOptionsResponse = {
  options: Record<string, Array<string | number>>;
  model_version: string;
  approval_threshold: number;
};

async function request<T>(path: string, init?: RequestInit, lang?: string): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(init?.headers as Record<string, string> | undefined),
  };
  if (lang) {
    headers["X-Lang"] = lang;
    headers["Accept-Language"] = lang;
  }

  const res = await fetch(`${API_BASE}${path}`, {
    ...init,
    headers,
  });
  if (!res.ok) {
    let detail = `Request failed (${res.status})`;
    try {
      const data = await res.json();
      if (typeof data.detail === "string") detail = data.detail;
      else if (Array.isArray(data.detail)) {
        detail = data.detail.map((d: { msg?: string }) => d.msg || JSON.stringify(d)).join("; ");
      }
    } catch {
      /* ignore */
    }
    throw new Error(detail);
  }
  return res.json() as Promise<T>;
}

export function fetchFormOptions() {
  return request<FormOptionsResponse>("/api/meta/form-options");
}

export function submitPrediction(payload: ApplicationPayload, lang?: string) {
  return request<PredictionResult>(
    "/api/predict",
    {
      method: "POST",
      body: JSON.stringify(payload),
    },
    lang,
  );
}

export function fetchPrediction(id: string, lang?: string) {
  return request<PredictionResult>(`/api/predictions/${id}`, undefined, lang);
}
