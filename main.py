import asyncio
import cmd
import subprocess

import GPUtil
import psutil


class Cli(cmd.Cmd):

    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = "> "
        self.intro = "Добро пожаловать\nДля справки наберите 'help'"
        self.doc_header = "Доступные команды (для справки по конкретной команде наберите 'help _команда_')"

    def do_show_cpu(self, args) -> None:
        """show_cpu - нагрузка на процессоры"""
        print("CPU (%):", psutil.cpu_percent(interval=1))

    def do_show_mem(self, args) -> None:
        """show_mem - использование RAM"""
        ram = psutil.virtual_memory()
        print("RAM usage (%):", ram.percent)
        print("RAM used (GB):", round(ram.used / 1e9, 2))

    def do_show_disk(self, args) -> None:
        """show_disk - свободное место на диске"""
        GB = 1073741824
        print(
            "Всего места:", "{0:.2f} GB".format(int(psutil.disk_usage("C:\\")[0]) / GB)
        )
        print(
            "Всего используется:",
            "{0:.2f} GB".format(int(psutil.disk_usage("C:\\")[1]) / GB),
        )
        print(
            "Всего свободно:",
            "{0:.2f} GB".format(int(psutil.disk_usage("C:\\")[2]) / GB),
        )
        print(
            "Всего используется (%):",
            "{} %".format(psutil.disk_usage("C:\\")[3]),
        )

    def do_show_gpu(self, args) -> None:
        """show_gpu - параметры видеокарты"""
        gpus = GPUtil.getGPUs()
        if gpus:
            for gpu in gpus:
                print(f"GPU ID: {gpu.id}")
                print(f"Название: {gpu.name}")
                print(f"Загрузка: {gpu.load*100:.2f}%")
                print(f"Использование памяти: {gpu.memoryUtil*100:.2f}%")
                print(f"Температура: {gpu.temperature:.2f}°C")

        else:
            print("GPU не обнаружено.")

    def do_show_net(self, args) -> None:
        """show_net - сетевые параметры"""
        data = subprocess.check_output(
            ["ipconfig", "/all"], encoding="cp866", errors="ignore"
        ).split("\n")
        for line in data:
            print(line.strip())

    def do_show_log(self, args) -> None:
        """show_log - системный журнал"""
        for p in psutil.process_iter(["name", "open_files"]):
            for file in p.info["open_files"] or []:
                if file.path.endswith(".log"):
                    print("%-5s %-10s %s" % (p.pid, p.info["name"][:10], file.path))

    def default(self, line) -> None:
        print("Несуществующая команда")

    def do_exit(self, args) -> bool:
        """exit - выход из программы"""
        print("Выход...")
        return True


class CliAscynio(Cli):
    def do_show_all(self, args) -> None:
        """show_all - информация об ПК"""
        asyncio.run(self._run_show_all())

    async def _run_show_all(self):
        await asyncio.to_thread(self.do_show_cpu, "")
        await asyncio.to_thread(self.do_show_gpu, "")
        await asyncio.to_thread(self.do_show_mem, "")
        await asyncio.to_thread(self.do_show_disk, "")


if __name__ == "__main__":
    cli = CliAscynio()
    try:
        cli.cmdloop()
    except KeyboardInterrupt:
        print("завершение сеанса...")
