/*
 * Blackpill Testbench - Zephyr Shell command tree.
 *
 * Implements the `tb` root command described in docs/Protocol_Spec.md:
 *   tb gpio set <pin_alias> <0|1>
 *   tb gpio get <pin_alias>
 *   tb pwm  set <pin_alias> <freq_hz> <duty_percent>
 *   tb adc  read <pin_alias>
 *
 * Pin aliases resolve to the &zephyr_user node in app.overlay.
 *
 * STATUS: scaffold. Handlers parse + validate args and emit the protocol
 * response strings (OK / VAL: / ERROR:). Hardware calls are marked TODO.
 * Owner: Mostafa (firmware layer).
 */
#include <zephyr/kernel.h>
#include <zephyr/shell/shell.h>
#include <zephyr/drivers/gpio.h>
#include <zephyr/drivers/pwm.h>
#include <zephyr/drivers/adc.h>
#include <zephyr/devicetree.h>
#include <stdlib.h>

#define ZEPHYR_USER_NODE DT_PATH(zephyr_user)

/* ---- Resolve logical endpoints from devicetree (app.overlay) ----
 * TODO(firmware/Mostafa): populate these spec arrays with the *_DT_SPEC_GET_BY_IDX
 * macros and use them in the handlers below.
 *
 *   static const struct gpio_dt_spec tb_out[] = {
 *       GPIO_DT_SPEC_GET_BY_IDX(ZEPHYR_USER_NODE, tb_out_gpios, 0), ...
 *   };
 *   static const struct gpio_dt_spec tb_in[]  = { ... tb_in_gpios ... };
 *   static const struct pwm_dt_spec  tb_pwm[] = { PWM_DT_SPEC_GET_BY_IDX(...), ... };
 *   static const struct adc_dt_spec  tb_adc[] = { ADC_DT_SPEC_GET_BY_IDX(...), ... };
 */

/* Map a "tb_out_3" style alias to a 0-based index. Returns -1 on bad format. */
static int alias_index(const char *alias, const char *prefix)
{
    size_t plen = strlen(prefix);
    if (strncmp(alias, prefix, plen) != 0) {
        return -1;
    }
    int n = atoi(alias + plen);      /* "tb_out_" -> "3" */
    return (n >= 1) ? (n - 1) : -1;  /* 1-based alias -> 0-based index */
}

/* ---------------- GPIO ---------------- */
static int cmd_gpio_set(const struct shell *sh, size_t argc, char **argv)
{
    int idx = alias_index(argv[1], "tb_out_");
    if (idx < 0) {
        shell_print(sh, "ERROR: Pin alias not found.");
        return -EINVAL;
    }
    int state = atoi(argv[2]);
    if (state != 0 && state != 1) {
        shell_print(sh, "ERROR: state must be 0 or 1.");
        return -EINVAL;
    }
    /* TODO(firmware/Mostafa): gpio_pin_set_dt(&tb_out[idx], state); */
    shell_print(sh, "OK");
    return 0;
}

static int cmd_gpio_get(const struct shell *sh, size_t argc, char **argv)
{
    int idx = alias_index(argv[1], "tb_in_");
    if (idx < 0) {
        shell_print(sh, "ERROR: Pin alias not found.");
        return -EINVAL;
    }
    int val = 0; /* TODO: val = gpio_pin_get_dt(&tb_in[idx]); */
    shell_print(sh, "VAL: %d", val);
    return 0;
}

/* ---------------- PWM ---------------- */
static int cmd_pwm_set(const struct shell *sh, size_t argc, char **argv)
{
    int idx = alias_index(argv[1], "tb_pwm_");
    if (idx < 0) {
        shell_print(sh, "ERROR: Pin alias not found.");
        return -EINVAL;
    }
    uint32_t freq = strtoul(argv[2], NULL, 10);
    uint32_t duty = strtoul(argv[3], NULL, 10);
    if (freq == 0 || duty > 100) {
        shell_print(sh, "ERROR: invalid frequency or duty cycle.");
        return -EINVAL;
    }
    /* TODO(firmware/Mostafa): convert freq+duty to period/pulse ns and call
     * pwm_set_dt(&tb_pwm[idx], period_ns, pulse_ns); */
    shell_print(sh, "OK");
    return 0;
}

/* ---------------- ADC ---------------- */
static int cmd_adc_read(const struct shell *sh, size_t argc, char **argv)
{
    int idx = alias_index(argv[1], "tb_adc_");
    if (idx < 0) {
        shell_print(sh, "ERROR: Pin alias not found.");
        return -EINVAL;
    }
    int millivolts = 0; /* TODO: adc_read_dt + adc_raw_to_millivolts_dt(&tb_adc[idx], ...) */
    shell_print(sh, "VAL: %d mV", millivolts);
    return 0;
}

/* ---------------- Command tree registration ---------------- */
SHELL_STATIC_SUBCMD_SET_CREATE(sub_gpio,
    SHELL_CMD_ARG(set, NULL, "set <pin_alias> <0|1>", cmd_gpio_set, 3, 0),
    SHELL_CMD_ARG(get, NULL, "get <pin_alias>",       cmd_gpio_get, 2, 0),
    SHELL_SUBCMD_SET_END
);
SHELL_STATIC_SUBCMD_SET_CREATE(sub_pwm,
    SHELL_CMD_ARG(set, NULL, "set <pin_alias> <freq_hz> <duty_pct>", cmd_pwm_set, 4, 0),
    SHELL_SUBCMD_SET_END
);
SHELL_STATIC_SUBCMD_SET_CREATE(sub_adc,
    SHELL_CMD_ARG(read, NULL, "read <pin_alias>", cmd_adc_read, 2, 0),
    SHELL_SUBCMD_SET_END
);
SHELL_STATIC_SUBCMD_SET_CREATE(sub_tb,
    SHELL_CMD(gpio, &sub_gpio, "Digital I/O commands", NULL),
    SHELL_CMD(pwm,  &sub_pwm,  "PWM output commands",  NULL),
    SHELL_CMD(adc,  &sub_adc,  "Analog input commands", NULL),
    SHELL_SUBCMD_SET_END
);
SHELL_CMD_REGISTER(tb, &sub_tb, "Blackpill Testbench control", NULL);
