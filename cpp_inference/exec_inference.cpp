
#include <atomic>
#include <boost/range/join.hpp>
#include <iostream>
#include <math.h>
#include <signal.h>
#include <string>
#include <vector>

#include <monopod_sdk/monopod.hpp>
// #include <torch/script.h>

/**
 * @brief This boolean is here to kill cleanly the application upon ctrl+c
 */
std::atomic_bool StopDemos(false);

/**
 * @brief This function is the callback upon a ctrl+c call from the terminal.
 *
 * @param s
 */
void my_handler(int) { StopDemos = true; }

int main(int argc, char *argv[]) {
  // make sure we catch the ctrl+c signal to kill the application properly.
  struct sigaction sigIntHandler;
  sigIntHandler.sa_handler = my_handler;
  sigemptyset(&sigIntHandler.sa_mask);
  sigIntHandler.sa_flags = 0;
  sigaction(SIGINT, &sigIntHandler, NULL);
  StopDemos = false;

  // Make sure there is at least one argument.
  if (argc != 3) {
    std::cerr << "Expecting Script Usage: \n"
                 "\t exec_inference [Model Path] [Mode] \n\n"
                 "\t Model Path - Absolute Path to pytorch model. \n\n"
                 "\t Mode - Available monopod modes 'fixed', 'fixed_connector',"
                 " 'free', 'motor_board'."
              << std::endl;
    exit(-1);
  }

  // // Load policy network
  //
  // std::string path_to_network = argv[1] torch::jit::script::Module
  // policy_net; try {
  //   policy_net = torch::jit::load(path_to_network);
  // } catch (const c10::Error &e) {
  //   std::cerr << "error loading the model from path: " << srgc[1] <<
  //   std::endl; exit(-1);
  // }

  std::string mode_name = argv[2];
  transform(mode_name.begin(), mode_name.end(), mode_name.begin(), toupper);

  std::unordered_map<std::string, monopod_drivers::Mode> get_mode = {
      {"FREE", monopod_drivers::Mode::FREE},
      {"FIXED_CONNECTOR", monopod_drivers::Mode::FIXED_CONNECTOR},
      {"FIXED", monopod_drivers::Mode::FIXED},
      {"MOTOR_BOARD", monopod_drivers::Mode::MOTOR_BOARD}};

  if (!get_mode.count(mode_name)) {
    std::cerr << "Provided mode '" << mode_name
              << "' not valid.\n"
                 "\t Mode - Available monopod modes 'fixed', 'fixed_connector',"
                 " 'free', 'motor_board'."
              << std::endl;
    exit(-1);
  }

  monopod_drivers::Mode mode = monopod_drivers::Mode::MOTOR_BOARD;

  monopod_drivers::Monopod monopod;
  rt_printf("initialized monopod sdk \n");
  monopod.initialize(mode, true);
  monopod.start_loop();

  real_time_tools::Spinner time_spinner;
  time_spinner.set_period(0.001); // 1kz loop

  while (!StopDemos) {

    // This does the same thing as [*poss, *vels]
    auto input_data = boost::copy_range<std::vector<double>>(boost::join(
        monopod.get_positions().value(), monopod.get_velocities().value()));

    // for (auto data : input_data) {
    //   std::cout << data;
    // }
    // std::cout << std::endl;

    // // Create inputs for model
    // std::vector<torch::jit::IValue> inputs;
    // torch::Tensor input_data =
    //     torch::from_blob(input_data.data(), {input_data.size()})
    //         .to(torch::kInt64);
    //
    // // Print output of model
    // auto output = policy_net.forward(inputs);
    // // std::cout << output.slice(/*dim=*/1, /*start=*/0, /*end=*/5) << '\n';
    // std::cout << output;

    /**
     * TODO: Set and send ouput torques to the robot
     * TODO: Need to guarntee the outputs and inputs to the model have the same
     * form as expected.
     */

    time_spinner.spin();
  }

  return 0;
}
