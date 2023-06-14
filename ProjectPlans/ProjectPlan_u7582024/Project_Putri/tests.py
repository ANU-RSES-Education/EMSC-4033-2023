import job_xml_generator as jxg
import user_input as ipt
import os
import unittest
from unittest.mock import patch, mock_open

class TestJobXmlGenerator(unittest.TestCase):

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '1'])
    def test_cost_type_pick(self, mock_input):
        self.assertEqual(ipt.cost_type_pick(), 'aggregated')
        self.assertEqual(ipt.cost_type_pick(), 'per_asset')
        self.assertEqual(ipt.cost_type_pick(), 'per_area')
        self.assertEqual(ipt.cost_type_pick(), 'aggregated')

    @patch('builtins.input', side_effect=['1', '2', 'a','1'])
    def test_area_type_pick(self, mock_input):
        self.assertEqual(ipt.area_type_pick(), 'aggregated')
        self.assertEqual(ipt.area_type_pick(), 'per_asset')
        self.assertEqual(ipt.area_type_pick(), 'aggregated')

    @patch('builtins.input', side_effect=['1', '2', '3', '4', '5'])
    def test_loss_cat_pick(self, mock_input):
        self.assertEqual(ipt.loss_cat_pick(), 'structural')
        self.assertEqual(ipt.loss_cat_pick(), 'nonstructural')
        self.assertEqual(ipt.loss_cat_pick(), 'business_interuption')
        self.assertEqual(ipt.loss_cat_pick(), 'contents')
        self.assertEqual(ipt.loss_cat_pick(), 'occupants')

    @patch('builtins.input', side_effect=['10','11.5','20'])
    def test_check_number(self, mock_input):
        self.assertEqual(ipt.check_number("Enter number: "), '10.0')
        self.assertEqual(ipt.check_number("Enter number: ", int_num=True), '20')

    @patch('builtins.input', side_effect=['valid_text'])
    def test_text_input(self, mock_input):
        self.assertEqual(ipt.text_input("Enter text: "), 'valid_text')
    
    @patch('builtins.input', side_effect=['y', 'n'])
    def test_yes_no_input(self, mock_input):
        self.assertEqual(ipt.yes_no_input("Yes or no? "), 'y')
        self.assertEqual(ipt.yes_no_input("Yes or no? "), 'n')

    @patch('builtins.input', side_effect=['absolute', 'relative'])
    def test_absolute_relative_input(self, mock_input):
        self.assertEqual(ipt.absolute_relative_input("Absolute or relative? "), 'absolute')
        self.assertEqual(ipt.absolute_relative_input("Absolute or relative? "), 'relative')

    @patch('builtins.input', side_effect=['y', '1', 'y', 'n', 'n'])
    def test_structural_cost_input(self, mock_input):
        self.assertEqual(ipt.structural_cost_input(), ('aggregated', 'y', None, None))
        
    @patch('builtins.input', side_effect=['y', '1'])
    def test_non_structural_cost_input(self, mock_input):
        self.assertEqual(ipt.non_structural_cost_input(), 'aggregated')
        
    @patch('builtins.input', side_effect=['y', '1'])
    def test_business_cost_input(self, mock_input):
        self.assertEqual(ipt.business_cost_input(), 'aggregated')

    @patch('builtins.input', side_effect=['y', '1'])
    def test_content_cost_input(self, mock_input):
        self.assertEqual(ipt.content_cost_input(), 'aggregated')

    @patch('builtins.input', return_value='n')
    def test_create_job_ini(self,mock_input):
        # Input parameters
        job_desc = "Test Job"
        rupture_mesh_spacing = 2
        ref_vs30 = 760
        depth_2pt5 = 5.0
        depth_1pt0 = 50.0
        gmpe = "gmpe_model"
        trunc_level = 3
        max_distance = 300
        num_gmf = 1

        output_folder = 'output'

        # Expected results in the job.ini
        expected_lines = [
            '[general]\n',
            f'description = {job_desc}\n',
            'calculation_mode = scenario_damage\n',
            'random_seed = 3\n',
            '\n[Rupture information]\n',
            'rupture_model_file = rupture_model.xml\n',
            f'rupture_mesh_spacing = {rupture_mesh_spacing}\n',
            '\n[Hazard sites]\n',
            '\n[Exposure model]\n',
            'exposure_file = exposure_model.xml\n',
            '\n[Fragility model]\n',
            'structural_fragility_file = fragility_model.xml\n',
            '\n[Site conditions]\n',
            'reference_vs30_type = measured\n',
            f'reference_vs30_value = {ref_vs30}\n',
            f'reference_depth_to_2pt5km_per_sec = {depth_2pt5}\n',
            f'reference_depth_to_1pt0km_per_sec = {depth_1pt0}\n',
            '\n[Calculation parameters]\n',
            f'truncation_level = {trunc_level}\n',
            f'maximum_distance = {max_distance}\n',
            f'gsim = {gmpe}\n',
            f'number_of_ground_motion_fields = {num_gmf}\n',
            '\n[output]\n',
            f'export_dir = {os.path.join(os.getcwd(), output_folder)}\n'
        ]
        
        # Mocking the saving of the file, and open it as mocked_open
        with patch('builtins.open', mock_open()) as mocked_open:
            jxg.create_job_ini(job_desc, rupture_mesh_spacing, ref_vs30, depth_2pt5, depth_1pt0, gmpe, trunc_level, max_distance, num_gmf)

        # Checking if the mocked file is supposedly save in the expected path
        expected_file_path = os.path.join('data', "job.ini")
        mocked_open.assert_called_once_with(expected_file_path, 'w')

        # Checking each lines of the mock file with the expected lines
        actual_lines = [call.args[0] for call in mocked_open().write.call_args_list]
        self.assertEqual(expected_lines, actual_lines)

if __name__ == '__main__':
    unittest.main()