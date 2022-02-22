using FF7R_MeshImporter_GUI.Properties;
using Microsoft.WindowsAPICodePack.Dialogs;

namespace FF7R_MeshImporter_GUI
{
    public partial class Form1 : Form
    {
        string SetFFDir = Settings.Default.FFInputPath;
        string SetUEDir = Settings.Default.UEInputPath;
        string SetOutDir = Settings.Default.OutputPath;

        public Form1()
        {
            InitializeComponent();
        }
        //
        //Base mode selection

        private void radioButton1_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton1.Checked)
            {
                radioButtonMdInject.Checked = true;
                {
                    foreach (Control ctrl in groupBoxUEOpt.Controls)
                    {
                        if (ctrl is TextBox)
                        {
                            TextBox textBox = (TextBox)ctrl;
                            textBox.Text = null;
                        }
                        if (ctrl is ComboBox)
                        {
                            ComboBox comboBox = (ComboBox)ctrl;
                            comboBox.SelectedIndex = -1;
                        }
                        if (ctrl is CheckBox)
                        {
                            CheckBox checkBox = (CheckBox)ctrl;
                            checkBox.Checked = false;
                        }
                        if (ctrl is RadioButton)
                        {
                            RadioButton radioButton = (RadioButton)ctrl;
                            radioButton.Checked = false;
                        }
                        if (ctrl is ListBox)
                        {
                            ListBox listBox = (ListBox)ctrl;
                            listBox.ClearSelected();
                        }
                    }
                }

            }
        }

        private void radioButton2_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButton2.Checked)
            {
                radioButtonUEModeValid.Checked = true;
                {
                    foreach (Control ctrl in groupBox7RInject.Controls)
                    {
                        if (ctrl is TextBox)
                        {
                            TextBox textBox = (TextBox)ctrl;
                            textBox.Text = null;
                        }
                        if (ctrl is ComboBox)
                        {
                            ComboBox comboBox = (ComboBox)ctrl;
                            comboBox.SelectedIndex = -1;
                        }
                        if (ctrl is CheckBox)
                        {
                            CheckBox checkBox = (CheckBox)ctrl;
                            checkBox.Checked = false;
                        }
                        if (ctrl is RadioButton)
                        {
                            RadioButton radioButton = (RadioButton)ctrl;
                            radioButton.Checked = false;
                        }
                        if (ctrl is ListBox)
                        {
                            ListBox listBox = (ListBox)ctrl;
                            listBox.ClearSelected();
                        }
                    }

                }
                label1.Enabled = false;
                textBox7RInput.Enabled = false;
                button1.Enabled = false;
                groupBox7RInject.Visible = false;
                groupBoxUEOpt.Visible = true;
            }
            else
            {
                label1.Enabled = true;
                textBox7RInput.Enabled = true;
                button1.Enabled = true;
                groupBox7RInject.Visible = true;
                groupBoxUEOpt.Visible = false;
            }
        }

        //
        //FF7R File Input

        private void textBox1_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox1_DragOver(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
                e.Effect = DragDropEffects.Link;
            else
                e.Effect = DragDropEffects.None;
        }

        private void textBox1_DragDrop(object sender, DragEventArgs e)
        {
            var files = (string[])e.Data.GetData(DataFormats.FileDrop);

            foreach (var file in files)
            {
                if (System.IO.Path.GetExtension(file).Equals(".uexp", StringComparison.InvariantCultureIgnoreCase))
                {
                    textBox7RInput.Text = file;
                }
                else
                {
                    MessageBox.Show("Not a .uexp file");
                }
            }
        }

        private void button1_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog ffdialog = new OpenFileDialog())
            {
                if (string.IsNullOrEmpty(textBox7RInput.Text))
                {
                    if (string.IsNullOrEmpty(Settings.Default.FFInputPath))
                    {
                        ffdialog.InitialDirectory = Path.GetDirectoryName(Application.ExecutablePath);
                    }
                    else
                    {
                        ffdialog.InitialDirectory = SetFFDir;
                    }
                }
                else
                {
                    ffdialog.InitialDirectory = Path.GetDirectoryName(textBox7RInput.Text);
                }
                ffdialog.Filter = "UEXP Files|*.uexp";
                {
                    if (ffdialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                    {
                        textBox7RInput.Text = ffdialog.FileName;
                    }
                }
            }
        }
        //
        //4.18 Input
        private void textBox2_TextChanged(object sender, EventArgs e)
        {

        }

        private void textBox2_DragOver(object sender, DragEventArgs e)
        {
            if (e.Data.GetDataPresent(DataFormats.FileDrop))
                e.Effect = DragDropEffects.Link;
            else
                e.Effect = DragDropEffects.None;
        }

        private void textBox2_DragDrop(object sender, DragEventArgs e)
        {
            var files = (string[])e.Data.GetData(DataFormats.FileDrop);

            foreach (var file in files)
            {
                if (System.IO.Path.GetExtension(file).Equals(".uexp", StringComparison.InvariantCultureIgnoreCase))
                {
                    textBoxUEInput.Text = file;
                }
                else
                {
                    MessageBox.Show("Not a .uexp file");
                }
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            using (OpenFileDialog uedialog = new OpenFileDialog())
            {
                if (string.IsNullOrEmpty(textBoxUEInput.Text))
                {
                    if (string.IsNullOrEmpty(Settings.Default.UEInputPath))
                    {
                        uedialog.InitialDirectory = Path.GetDirectoryName(Application.ExecutablePath);
                    }
                    else
                    {
                        uedialog.InitialDirectory = SetUEDir;
                    }
                }
                else
                {
                    uedialog.InitialDirectory = Path.GetDirectoryName(textBoxUEInput.Text);
                }
                uedialog.Filter = "UEXP Files|*.uexp";
                {
                    if (uedialog.ShowDialog() == System.Windows.Forms.DialogResult.OK)
                    {
                        textBoxUEInput.Text = uedialog.FileName;
                    }
                }
            }
        }
        //
        //Output
        private void button3_Click(object sender, EventArgs e)
        {
            CommonOpenFileDialog outdialog = new CommonOpenFileDialog();
            if (string.IsNullOrEmpty(textBoxOutput.Text))
            {
                if (string.IsNullOrEmpty(Settings.Default.OutputPath))
                {
                    outdialog.InitialDirectory = Path.GetDirectoryName(Application.ExecutablePath);
                }
                else
                {
                    outdialog.InitialDirectory = SetOutDir;
                }
            }
            else
            {
                outdialog.InitialDirectory = textBoxOutput.Text;
            }
            outdialog.IsFolderPicker = true;
            outdialog.Title = "Select Output Folder";
            if (outdialog.ShowDialog() == CommonFileDialogResult.Ok)
            {
                textBoxOutput.Text = outdialog.FileName;
            }
        }

        //
        //Option Modes


        private void radioButtonMdLODs_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButtonMdLODs.Checked)
            {
                label2.Enabled = false;
                textBoxUEInput.Enabled = false;
                button2.Enabled = false;
                checkedListBox7ROpt.Enabled = false;
            }
            else
            {
                label2.Enabled = true;
                textBoxUEInput.Enabled = true;
                button2.Enabled = true;
                checkedListBox7ROpt.Enabled = true;
            }
        }

        private void radioButtonMdDump_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButtonMdDump.Checked)
            {
                label2.Enabled = false;
                textBoxUEInput.Enabled = false;
                button2.Enabled = false;
                checkedListBox7ROpt.Enabled = false;
            }
            else
            {
                label2.Enabled = true;
                textBoxUEInput.Enabled = true;
                button2.Enabled = true;
                checkedListBox7ROpt.Enabled = true;
            }
        }

        private void radioButtonMdValid_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButtonMdValid.Checked)
            {
                label2.Enabled = false;
                textBoxUEInput.Enabled = false;
                button2.Enabled = false;
                checkedListBox7ROpt.Enabled = false;
            }
            else
            {
                label2.Enabled = true;
                textBoxUEInput.Enabled = true;
                button2.Enabled = true;
                checkedListBox7ROpt.Enabled = true;
            }
        }

        private void radioButtonMdInject_CheckedChanged(object sender, EventArgs e)
        {
            if (radioButtonMdInject.Checked)
            {
                label2.Enabled = true;
                textBoxUEInput.Enabled = true;
                button2.Enabled = true;
                checkedListBox7ROpt.Enabled = true;
            }
        }

        private void checkedListBox1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }

        //
        //Injection

        private void button4_Click(object sender, EventArgs e)
        {
            string strFFInput = textBox7RInput.Text;
            string strUEInput = textBoxUEInput.Text;
            string strOutput = textBoxOutput.Text;

            string mode = "";
            string only_mesh = "";
            string dont_remove_KDI = "";

            //check if main.exe exists
            string strApp = "./src/main.exe";

            if (!File.Exists(strApp))
            {
                strApp = "python ./src/main.py";
            }
            else
            {
                strApp = "call \"" + strApp + "\"";
            }

            if (radioButton1.Checked) //FF7R Injection
            {
                //set mode
                mode = "import";
                if (radioButtonMdLODs.Checked)
                {
                    mode = "removeLOD";
                }
                else if (radioButtonMdValid.Checked)
                {
                    mode = "valid";
                }
                else if (radioButtonMdDump.Checked)
                {
                    mode = "dumpBuffers";
                }

                //set options
                only_mesh = "--only_mesh";
                foreach (int id in checkedListBox7ROpt.CheckedIndices)
                {
                    if (id == 0) //Import Bones
                    {
                        only_mesh = "";
                    }
                    if (id == 1) //Don't Remove KDI
                    {
                        dont_remove_KDI = "--dont_remove_KDI";
                    }
                }
                string strCmdText = "/c " + strApp + " "
    + "\"" + strFFInput + "\"" + " " + "\"" + strUEInput + "\"" + " " + "\"" + strOutput + "\"" + " --mode=" + mode + " "
    + only_mesh + " " + dont_remove_KDI + " --verbose";
                System.Diagnostics.Process.Start("CMD.exe", strCmdText);
            }
            else if (radioButton2.Checked) //UE4.18
            {
                //set mode
                if (radioButtonUEModeValid.Checked)
                {
                    mode = "valid";
                }
                else if (radioButtonUEModeDump.Checked)
                {
                    mode = "dumpBuffers";
                }

                string strCmdText = "/c " + strApp + " "
    + "\"" + strUEInput + "\"" + " " + "\"" + strOutput + "\"" + " --mode=" + mode + " "
    + only_mesh + " " + dont_remove_KDI + " --verbose";
                System.Diagnostics.Process.Start("CMD.exe", strCmdText);

            }
            
        }



            //
            // Settings

            private void savePathSettingsToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Settings.Default.FFInputPath = Path.GetDirectoryName(textBox7RInput.Text);
            Settings.Default.UEInputPath = Path.GetDirectoryName(textBoxUEInput.Text);
            Settings.Default.OutputPath = Path.GetDirectoryName(textBoxOutput.Text);
            Settings.Default.Save();
        }

        private void aboutToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AboutBox1 a = new AboutBox1();
            a.Show();
        }
    }
}