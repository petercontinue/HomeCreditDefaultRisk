import { useEffect, useState } from "react";
import { useForm } from "react-hook-form";
import { useNavigate } from "react-router-dom";
import { fetchFormOptions, submitPrediction } from "../api/client";
import { useI18n } from "../i18n/I18nProvider";
import { defaultFormValues, type LoanFormValues } from "../types/form";

const WEEKDAYS = [
  "SUNDAY",
  "MONDAY",
  "TUESDAY",
  "WEDNESDAY",
  "THURSDAY",
  "FRIDAY",
  "SATURDAY",
];

export function ApplyPage() {
  const navigate = useNavigate();
  const { t, locale } = useI18n();
  const [options, setOptions] = useState<Record<string, Array<string | number>>>({});
  const [loadingOptions, setLoadingOptions] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [step, setStep] = useState(0);

  const {
    register,
    handleSubmit,
    watch,
    formState: { errors },
  } = useForm<LoanFormValues>({ defaultValues: defaultFormValues });

  const ownCar = watch("flag_own_car");

  useEffect(() => {
    fetchFormOptions()
      .then((res) => setOptions(res.options))
      .catch((err: Error) => setError(err.message))
      .finally(() => setLoadingOptions(false));
  }, []);

  const onSubmit = async (values: LoanFormValues) => {
    setSubmitting(true);
    setError(null);
    try {
      const weekday = WEEKDAYS[new Date().getDay()];
      const result = await submitPrediction(
        {
          ...values,
          own_car_age: values.flag_own_car === "Y" ? values.own_car_age : null,
          amt_goods_price: values.amt_goods_price || values.amt_credit,
          occupation_type: values.occupation_type || null,
          weekday_appr_process_start: weekday,
          lang: locale,
        },
        locale,
      );
      sessionStorage.setItem("lastPrediction", JSON.stringify(result));
      navigate(`/result/${result.application_id}`);
    } catch (err) {
      setError(err instanceof Error ? err.message : t.apply.submitFailed);
    } finally {
      setSubmitting(false);
    }
  };

  const opt = (key: string) => options[key] || [];
  const steps = [t.apply.stepPersonal, t.apply.stepIncome, t.apply.stepLoan];

  if (loadingOptions) {
    return (
      <main className="page">
        <p className="muted">{t.apply.loading}</p>
      </main>
    );
  }

  return (
    <main className="page apply-page">
      <header className="page-header">
        <p className="brand-sm">{t.brand}</p>
        <h1>{t.apply.title}</h1>
        <p className="lede">{t.apply.lede}</p>
        <div className="stepper" aria-label={t.apply.progress}>
          {steps.map((label, i) => (
            <button
              key={label}
              type="button"
              className={`step-chip ${i === step ? "active" : ""} ${i < step ? "done" : ""}`}
              onClick={() => setStep(i)}
            >
              {i + 1}. {label}
            </button>
          ))}
        </div>
      </header>

      <form className="apply-form" onSubmit={handleSubmit(onSubmit)}>
        {step === 0 && (
          <section className="form-section">
            <h2>{t.apply.personalTitle}</h2>
            <div className="grid-2">
              <label>
                {t.apply.gender}
                <select {...register("code_gender", { required: true })}>
                  {opt("CODE_GENDER").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {v === "F" ? t.apply.female : t.apply.male}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.age}
                <input
                  type="number"
                  step="0.1"
                  {...register("age_years", { valueAsNumber: true, min: 18, max: 100, required: true })}
                />
              </label>
              <label>
                {t.apply.familyStatus}
                <select {...register("name_family_status", { required: true })}>
                  {opt("NAME_FAMILY_STATUS").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.education}
                <select {...register("name_education_type", { required: true })}>
                  {opt("NAME_EDUCATION_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.housing}
                <select {...register("name_housing_type", { required: true })}>
                  {opt("NAME_HOUSING_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.ownRealty}
                <select {...register("flag_own_realty", { required: true })}>
                  <option value="Y">{t.apply.yes}</option>
                  <option value="N">{t.apply.no}</option>
                </select>
              </label>
              <label>
                {t.apply.ownCar}
                <select {...register("flag_own_car", { required: true })}>
                  <option value="N">{t.apply.no}</option>
                  <option value="Y">{t.apply.yes}</option>
                </select>
              </label>
              {ownCar === "Y" && (
                <label>
                  {t.apply.carAge}
                  <input
                    type="number"
                    step="0.1"
                    {...register("own_car_age", { valueAsNumber: true, min: 0, max: 80 })}
                  />
                </label>
              )}
              <label>
                {t.apply.children}
                <input
                  type="number"
                  {...register("cnt_children", { valueAsNumber: true, min: 0, max: 20, required: true })}
                />
              </label>
              <label>
                {t.apply.familyMembers}
                <input
                  type="number"
                  step="1"
                  {...register("cnt_fam_members", { valueAsNumber: true, min: 1, max: 30, required: true })}
                />
              </label>
              <label>
                {t.apply.accompaniedBy}
                <select {...register("name_type_suite", { required: true })}>
                  {opt("NAME_TYPE_SUITE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.regionRating}
                <select {...register("region_rating_client", { valueAsNumber: true, required: true })}>
                  {opt("REGION_RATING_CLIENT").map((v) => (
                    <option key={String(v)} value={Number(v)}>
                      {String(v)} (
                      {Number(v) === 1
                        ? t.apply.ratingBetter
                        : Number(v) === 2
                          ? t.apply.ratingAverage
                          : t.apply.ratingWeaker}
                      )
                    </option>
                  ))}
                </select>
              </label>
            </div>
            <div className="check-row">
              <label className="check">
                <input type="checkbox" {...register("flag_email")} /> {t.apply.provideEmail}
              </label>
              <label className="check">
                <input type="checkbox" {...register("flag_phone")} /> {t.apply.providePhone}
              </label>
              <label className="check">
                <input type="checkbox" {...register("flag_work_phone")} /> {t.apply.provideWorkPhone}
              </label>
            </div>
          </section>
        )}

        {step === 1 && (
          <section className="form-section">
            <h2>{t.apply.incomeTitle}</h2>
            <div className="grid-2">
              <label>
                {t.apply.annualIncome}
                <input
                  type="number"
                  {...register("amt_income_total", { valueAsNumber: true, min: 1, required: true })}
                />
              </label>
              <label>
                {t.apply.incomeType}
                <select {...register("name_income_type", { required: true })}>
                  {opt("NAME_INCOME_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.yearsEmployed}
                <input
                  type="number"
                  step="0.1"
                  {...register("employment_years", { valueAsNumber: true, min: 0, max: 60, required: true })}
                />
              </label>
              <label>
                {t.apply.occupation}
                <select {...register("occupation_type")}>
                  <option value="">{t.apply.occupationEmpty}</option>
                  {opt("OCCUPATION_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label className="full">
                {t.apply.organization}
                <select {...register("organization_type", { required: true })}>
                  {opt("ORGANIZATION_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
            </div>
          </section>
        )}

        {step === 2 && (
          <section className="form-section">
            <h2>{t.apply.loanTitle}</h2>
            <div className="grid-2">
              <label>
                {t.apply.contractType}
                <select {...register("name_contract_type", { required: true })}>
                  {opt("NAME_CONTRACT_TYPE").map((v) => (
                    <option key={String(v)} value={String(v)}>
                      {String(v)}
                    </option>
                  ))}
                </select>
              </label>
              <label>
                {t.apply.requestedAmount}
                <input
                  type="number"
                  {...register("amt_credit", { valueAsNumber: true, min: 1, required: true })}
                />
              </label>
              <label>
                {t.apply.annuity}
                <input
                  type="number"
                  {...register("amt_annuity", { valueAsNumber: true, min: 1, required: true })}
                />
              </label>
              <label>
                {t.apply.goodsPrice}
                <input
                  type="number"
                  {...register("amt_goods_price", { valueAsNumber: true, min: 1 })}
                />
              </label>
            </div>
            <p className="hint">{t.apply.annuityHint}</p>
          </section>
        )}

        {Object.keys(errors).length > 0 && (
          <p className="form-error">{t.apply.validationError}</p>
        )}
        {error && <p className="form-error">{error}</p>}

        <div className="form-actions">
          {step > 0 ? (
            <button type="button" className="btn btn-ghost" onClick={() => setStep((s) => s - 1)}>
              {t.apply.back}
            </button>
          ) : (
            <span />
          )}
          {step < 2 ? (
            <button type="button" className="btn btn-primary" onClick={() => setStep((s) => s + 1)}>
              {t.apply.next}
            </button>
          ) : (
            <button type="submit" className="btn btn-primary" disabled={submitting}>
              {submitting ? t.apply.assessing : t.apply.submit}
            </button>
          )}
        </div>
      </form>
    </main>
  );
}
