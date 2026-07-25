export type Locale = "en" | "zh-CN" | "zh-TW" | "ja" | "ko";

export const LOCALES: { code: Locale; label: string }[] = [
  { code: "en", label: "English" },
  { code: "zh-CN", label: "简体中文" },
  { code: "zh-TW", label: "繁體中文" },
  { code: "ja", label: "日本語" },
  { code: "ko", label: "한국어" },
];

export const LOCALE_TAG: Record<Locale, string> = {
  en: "en-US",
  "zh-CN": "zh-CN",
  "zh-TW": "zh-TW",
  ja: "ja-JP",
  ko: "ko-KR",
};

export type Dict = {
  brand: string;
  home: {
    title: string;
    lede: string;
    start: string;
    how: string;
    disclaimer: string;
    stepsTitle: string;
    step1Title: string;
    step1Desc: string;
    step2Title: string;
    step2Desc: string;
    step3Title: string;
    step3Desc: string;
  };
  apply: {
    title: string;
    lede: string;
    progress: string;
    stepPersonal: string;
    stepIncome: string;
    stepLoan: string;
    personalTitle: string;
    incomeTitle: string;
    loanTitle: string;
    loading: string;
    gender: string;
    female: string;
    male: string;
    age: string;
    familyStatus: string;
    education: string;
    housing: string;
    ownRealty: string;
    ownCar: string;
    yes: string;
    no: string;
    carAge: string;
    children: string;
    familyMembers: string;
    accompaniedBy: string;
    regionRating: string;
    ratingBetter: string;
    ratingAverage: string;
    ratingWeaker: string;
    provideEmail: string;
    providePhone: string;
    provideWorkPhone: string;
    annualIncome: string;
    incomeType: string;
    yearsEmployed: string;
    occupation: string;
    occupationEmpty: string;
    organization: string;
    contractType: string;
    requestedAmount: string;
    annuity: string;
    goodsPrice: string;
    annuityHint: string;
    validationError: string;
    submitFailed: string;
    back: string;
    next: string;
    submit: string;
    assessing: string;
  };
  result: {
    title: string;
    loading: string;
    approve: string;
    decline: string;
    riskLevel: string;
    defaultProb: string;
    requestedAmount: string;
    maxAmount: string;
    positives: string;
    concerns: string;
    suggestions: string;
    applicationId: string;
    model: string;
    reassess: string;
    assessAgain: string;
    backHome: string;
  };
  common: {
    language: string;
    requestFailed: string;
  };
};
