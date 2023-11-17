#!/usr/bin/python3

import argparse
import os
import random

class test_runner:

    def __init__(self):
        self.sim_dir = os.getcwd()
        self.elab_opts = ''
        self.defines = ''
        self.dump = ''
        self.__test_param = ''
        self.__common_param = ''
        self.__workarounds = '-warn_multiple_driver -V93 -ALLOWREDEFINITION -NAMEMAP_MIXGEN '

    def add_str_nl(self, str_to_add, add_str):
        str_to_add = f"{str_to_add}\n{add_str}" if str_to_add != "" else add_str
        return str_to_add

    def write_script_description(self):
        description = "Clean, Compile, Elaborate and Run simulation with provided test case."
        description = self.add_str_nl(description, "This"                                    )
        description = self.add_str_nl(description, "is"                                      )
        description = self.add_str_nl(description, "an"                                      )
        description = self.add_str_nl(description, "example"                                 )
        description = self.add_str_nl(description, "how"                                     )
        description = self.add_str_nl(description, "to"                                      )     
        description = self.add_str_nl(description, "add"                                     )
        description = self.add_str_nl(description, "description"                             )
        return description


    

    def run_cmd(self, cmd):
        if self.args.quiet_mode:
            cmd = cmd + " >/dev/null 2>&1"
        if not self.args.quiet_mode: print(cmd)
        result = os.system(cmd)
        if not self.args.quiet_mode: print("")
        if not self.args.quiet_mode: print("")
        if(result > 0):
            print(f"-- ERROR -- COMMAND FAILED with code {result}")
            print(f"Failure cmd was: '{cmd}'")
            if(self.args.no_continous_mode):
                    print("Continous mode disabled, exiting")
                    exit()

    #-----------------------------------------------------------------
    def parse_cmdline_args(self):
        script_desc = self.write_script_description()
        parser = argparse.ArgumentParser(description = script_desc, formatter_class = argparse.RawTextHelpFormatter)

        parser.add_argument('--test',           type=str, default="",                help="to provide test case name"                                               )
        parser.add_argument('--seed',           type=int, default=0,                 help="if 0 (default), then it will be overriden as random value"               )
        parser.add_argument('--verbosity',      type=str, default="UVM_LOW",         help="default=UVM_LOW"                                                         )
        parser.add_argument('--comp_folder',    type=str, default="compile",         help="default=compile"                                                         )
        parser.add_argument('--comp_rtl_str',   type=str, default="",                help="provide all rtl paths to compile"                                        )
        parser.add_argument('--comp_tb_str',    type=str, default="",                help="provide all tb  paths to compile"                                        )
        parser.add_argument('--elab_rtl_str',   type=str, default="",                help="provide all rtl paths to elaborate"                                      )
        parser.add_argument('--elab_tb_str',    type=str, default="",                help="provide all tb  paths to elaborate"                                      )
        parser.add_argument('--defines',        type=str, default="",                help="additional defines for elaboration phase"                                )
        parser.add_argument('--simargs',        type=str, default="",                help="additional arguments to run, like +UVM_TRACE_OBJECTIONS"                 )
        parser.add_argument('--cov',            action="store_true",                 help="enable coverage collection"                                              )
        parser.add_argument('--covfile',        type=str, default="",                help="provide coverage file"                                                   )
        parser.add_argument('--linedebug',      action="store_true",                 help="run with linedebug option"                                               )
        parser.add_argument("--gui",            action="store_true",                 help="run in GUI mode"                                                         )
        parser.add_argument("--run_n_exit",     action="store_true",                 help="if GUI mode, then run and exit"                                          )
        parser.add_argument('--clean',          action="store_true",                 help="to remove directories: comp_folder and test_runs"                        )
        parser.add_argument('--clean_all',      action="store_true",                 help="to remove directories: comp_folder, test_runs and tests_previous_version")
        parser.add_argument('--no_compile',     action="store_true",                 help="to skip compile rtl and tb"                                              )
        parser.add_argument('--no_compile_rtl', action="store_true",                 help="to skip compile rtl"                                                     )
        parser.add_argument('--no_run',         action="store_true",                 help="to not run test sim"                                                     )
        parser.add_argument('--no_backup',      action="store_true",                 help="to remove previous logs from a test case and run it one more time"       )
        parser.add_argument('--quiet_mode',     action="store_true",                 help="enable coverage collection"                                              )
        parser.add_argument('--no_continous_mode', action="store_true",              help="enable to stop test on a first failure"                                  )
        parser.add_argument('--c_compile_mode', type=str, default="baremetal",       help="compile SW examples, possible options: baremetal, freertos",             )
        parser.add_argument('--only_c_compile', action="store_true",                 help="script will only compile C code, then exit",                             )
        parser.add_argument('--c_compile',      action="store_true",                 help="senable c compilation",                                                  )
        parser.add_argument('--dump',           action="store_true",                 help="enable dump waveforms",                                                            )

        self.args, self.unknown_args = parser.parse_known_args()
        # if self.args.quiet_mode    : print("Test runs with quiet_mode == True -> most of prints from run_sim.py scripts are disabled")
        # else                       : print("Test runs with quiet_mode == False -> all prints from run_sim.py scripts are enabled")
        # self.print_args()

    
    def clean(self):
        pass

    def prepare_xrun_args(self, test_run_path = "test_runs"):
        self.test           = f"{self.args.test}"    if self.args.test    != ""   else ""
        self.seed           = f"{self.args.seed}"    if self.args.seed    != 0    else f"{random.randint(0, 99999)}"
        self.defines    = f" {self.args.defines}"      if self.args.defines != ""                else self.defines
        self.dump       = f" +define+TB_GEN_DUMP "      if self.args.dump    != 0                 else ""
        self.simargs    = f" {self.args.simargs}"      if self.args.simargs != ""                else ""
        self.coverage   = f" -covfile {self.sim_dir}/covspec -coverage all" if self.args.cov     else ""
        self.linedebug  = " -linedebug"                if self.args.linedebug                    else ""
        self.gui        = " -gui"                      if self.args.gui                          else ""
        self.run_n_exit = " -run -exit"                if self.args.gui and self.args.run_n_exit else ""

        self.comp_dir       = f"{self.sim_dir}/{self.args.comp_folder}"
        self.test_with_seed = f"{self.args.test}_{self.seed}"
        self.test_folder    = f"{test_run_path}/test_{self.test_with_seed}"
        self.test_dir       = f"{self.sim_dir}/{self.test_folder}"
        self.log_dir        = f"{self.test_dir}/log"

        self.uvm_home   =  " -uvm -uvmhome /tools/cdnc/xcelium/current/tools/methodology/UVM/CDNS-1.2/ -sysv -access +rw -timescale 1ns/1ns"
        # self.uvm_params = f" +UVM_TESTNAME={self.args.test} +UVM_VERBOSITY={self.args.verbosity}"
        self.uvm_params = ""

    def parse_args(self):
        self.parse_cmdline_args()
        self.clean()
        self.prepare_xrun_args()
    #-----------------------------------------------------------------


    def add_test_params(self, params):
        self.___test_param = params

    def add_common_params(self, params):
        self.__common_param = params



    #-----------------------------------------------------------------
    def check_args(self):
        pass

    def prepare_test_dir(self):
        self.is_test_dir_created    = os.path.isdir(self.test_dir)
        if self.args.no_run == False:
            if self.is_test_dir_created == True:
                os.system(f"rm -rf {self.test_dir}")
            os.system(f"mkdir -p {self.test_dir}")


    def prepare_test_backup(self):
        pass

    def remove_comp_dir(self):
        if self.args.no_compile == False and self.args.no_compile_rtl == False:
            os.system(f"rm -rf {self.comp_dir}")
            os.system(f"mkdir -p {self.comp_dir}")
        elif self.args.no_compile == False and self.args.no_compile_rtl == True:
            os.system(f"rm -rf {self.comp_dir}/tb_lib {self.comp_dir}/elab")

    def prepare_dirs(self):
        self.check_args()
        self.prepare_test_dir()
        self.prepare_test_backup()
        self.remove_comp_dir()
    #-----------------------------------------------------------------



    #-----------------------------------------------------------------
    def compile_rtl(self):
        if self.args.no_compile == False and self.args.no_compile_rtl == False:
            comp_rtl_str = "-incdir /users/mateuszn/repos/uvmp/rtl -f /users/mateuszn/repos/uvmp/rtl/rtl_flist.f"
            cmd = f"xrun -64bit -compile -fast_recompilation -xmlibdirname rtl_lib -xmlibdirpath {self.comp_dir} -work rtl -makelib comp_rtl {comp_rtl_str} -endlib -licqueue {self.linedebug} {self.__workarounds} {self.__common_param} {self.defines} {self.dump}"
            self.run_cmd(cmd)

    def compile_tb(self):
        pass

    def prepare_elab_opts(self):
        self.elab_opts = ' ' +  self.defines

    def elab_rtl(self):
        if self.args.no_compile == False:
            elab_rtl_str = "-incdir /users/mateuszn/repos/uvmp/rtl -f /users/mateuszn/repos/uvmp/rtl/rtl_flist.f"
            cmd = f"xrun  -elaborate -L {self.comp_dir}/rtl_lib/log {elab_rtl_str} -xmlibdirname elab -xmlibdirpath {self.comp_dir} -licqueue {self.linedebug} {self.__workarounds} {self.__common_param} {self.dump}"
            cmd = cmd + self.coverage + self.elab_opts
            self.run_cmd(cmd)

    def elab_tb(self):
        pass
    
    
    def compile_and_elaborate(self):
        os.chdir(self.comp_dir)
        self.compile_rtl()
        self.compile_tb()
        self.prepare_elab_opts()
        self.elab_rtl()
        self.elab_tb()
    #-----------------------------------------------------------------



    #-----------------------------------------------------------------
    def execute_test(self):
        if self.args.no_run == False:
            os.chdir(self.test_dir)
            os.system(f"mkdir -p {self.log_dir};")
            run_opts = self.uvm_params + self.gui + self.linedebug + self.coverage + self.simargs + self.run_n_exit
            print(f"Running test {self.test_with_seed}")
            if not self.args.quiet_mode: print("with additional arguments: " + run_opts)
            cmd = f"xrun -64bit -R -xmlibdirname elab -xmlibdirpath {self.comp_dir} -simtmp {self.log_dir} -seed {self.seed} -licqueue {self.__common_param}"
            cmd = cmd + run_opts
            self.run_cmd(cmd)


    def run_test(self):
        self.execute_test()
        os.chdir(self.sim_dir)
    #-----------------------------------------------------------------



if __name__ == '__main__':
    test_runner_i = test_runner()
    test_runner_i.parse_args()
    test_runner_i.prepare_dirs()
    test_runner_i.compile_and_elaborate()
    test_runner_i.run_test()