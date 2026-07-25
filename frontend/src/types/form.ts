export type LoanFormValues = {
  name_contract_type: "Cash loans" | "Revolving loans";
  code_gender: "F" | "M";
  flag_own_car: "N" | "Y";
  flag_own_realty: "N" | "Y";
  cnt_children: number;
  amt_income_total: number;
  amt_credit: number;
  amt_annuity: number;
  amt_goods_price: number;
  name_type_suite: string;
  name_income_type: string;
  name_education_type: string;
  name_family_status: string;
  name_housing_type: string;
  age_years: number;
  employment_years: number;
  own_car_age: number;
  occupation_type: string;
  cnt_fam_members: number;
  organization_type: string;
  region_rating_client: number;
  flag_email: boolean;
  flag_phone: boolean;
  flag_work_phone: boolean;
};

export const defaultFormValues: LoanFormValues = {
  name_contract_type: "Cash loans",
  code_gender: "F",
  flag_own_car: "N",
  flag_own_realty: "Y",
  cnt_children: 0,
  amt_income_total: 180000,
  amt_credit: 450000,
  amt_annuity: 22000,
  amt_goods_price: 450000,
  name_type_suite: "Unaccompanied",
  name_income_type: "Working",
  name_education_type: "Secondary / secondary special",
  name_family_status: "Married",
  name_housing_type: "House / apartment",
  age_years: 35,
  employment_years: 5,
  own_car_age: 5,
  occupation_type: "Laborers",
  cnt_fam_members: 2,
  organization_type: "Business Entity Type 3",
  region_rating_client: 2,
  flag_email: true,
  flag_phone: true,
  flag_work_phone: false,
};
