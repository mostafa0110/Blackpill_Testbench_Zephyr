/*
 * Blackpill Testbench - firmware entry point.
 * The real work happens in the Zephyr Shell command handlers (tb_shell.c).
 * main() just brings the system up and logs readiness.
 */
#include <zephyr/kernel.h>
#include <zephyr/logging/log.h>

LOG_MODULE_REGISTER(testbench, LOG_LEVEL_INF);

int main(void)
{
    LOG_INF("Blackpill Testbench ready. Use the 'tb' shell command tree.");
    /* Shell runs in its own thread; nothing to do here. */
    return 0;
}
