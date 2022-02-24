namespace FF7R_MeshImporter_GUI
{
    partial class Form1
    {
        /// <summary>
        ///  Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        ///  Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        ///  Required method for Designer support - do not modify
        ///  the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.textBox7RInput = new System.Windows.Forms.TextBox();
            this.textBoxUEInput = new System.Windows.Forms.TextBox();
            this.textBoxOutput = new System.Windows.Forms.TextBox();
            this.button1 = new System.Windows.Forms.Button();
            this.button2 = new System.Windows.Forms.Button();
            this.buttonSInject = new System.Windows.Forms.Button();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.button3 = new System.Windows.Forms.Button();
            this.menuStrip1 = new System.Windows.Forms.MenuStrip();
            this.fileToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.savePathSettingsToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.aboutToolStripMenuItem = new System.Windows.Forms.ToolStripMenuItem();
            this.radioButton1 = new System.Windows.Forms.RadioButton();
            this.radioButton2 = new System.Windows.Forms.RadioButton();
            this.groupBoxAppMode = new System.Windows.Forms.GroupBox();
            this.groupBox7RInject = new System.Windows.Forms.GroupBox();
            this.authorlabel4 = new System.Windows.Forms.Label();
            this.authortextBox1 = new System.Windows.Forms.TextBox();
            this.radioButtonMdValid = new System.Windows.Forms.RadioButton();
            this.radioButtonMdDump = new System.Windows.Forms.RadioButton();
            this.radioButtonMdLODs = new System.Windows.Forms.RadioButton();
            this.radioButtonMdInject = new System.Windows.Forms.RadioButton();
            this.checkedListBox7ROpt = new System.Windows.Forms.CheckedListBox();
            this.groupBoxUEOpt = new System.Windows.Forms.GroupBox();
            this.radioButtonUEModeValid = new System.Windows.Forms.RadioButton();
            this.radioButtonUEModeDump = new System.Windows.Forms.RadioButton();
            this.flowLayoutPanel1 = new System.Windows.Forms.FlowLayoutPanel();
            this.groupBox1 = new System.Windows.Forms.GroupBox();
            this.flowLayoutPanel2 = new System.Windows.Forms.FlowLayoutPanel();
            this.fontDialog1 = new System.Windows.Forms.FontDialog();
            this.richTextBox1 = new System.Windows.Forms.RichTextBox();
            this.menuStrip1.SuspendLayout();
            this.groupBoxAppMode.SuspendLayout();
            this.groupBox7RInject.SuspendLayout();
            this.groupBoxUEOpt.SuspendLayout();
            this.flowLayoutPanel1.SuspendLayout();
            this.groupBox1.SuspendLayout();
            this.flowLayoutPanel2.SuspendLayout();
            this.SuspendLayout();
            // 
            // textBox7RInput
            // 
            this.textBox7RInput.AccessibleDescription = "Base Game Input .uexp";
            this.textBox7RInput.AccessibleName = "7R Input";
            this.textBox7RInput.AllowDrop = true;
            this.textBox7RInput.Location = new System.Drawing.Point(177, 13);
            this.textBox7RInput.Name = "textBox7RInput";
            this.textBox7RInput.PlaceholderText = "Select 7R .uexp File Path or Drop File Here";
            this.textBox7RInput.Size = new System.Drawing.Size(418, 23);
            this.textBox7RInput.TabIndex = 1;
            this.textBox7RInput.DragDrop += new System.Windows.Forms.DragEventHandler(this.textBox1_DragDrop);
            this.textBox7RInput.DragOver += new System.Windows.Forms.DragEventHandler(this.textBox1_DragOver);
            // 
            // textBoxUEInput
            // 
            this.textBoxUEInput.AllowDrop = true;
            this.textBoxUEInput.Location = new System.Drawing.Point(177, 43);
            this.textBoxUEInput.Name = "textBoxUEInput";
            this.textBoxUEInput.PlaceholderText = "Select UE 4.18 .uexp File Path or Drop File Here";
            this.textBoxUEInput.Size = new System.Drawing.Size(418, 23);
            this.textBoxUEInput.TabIndex = 2;
            this.textBoxUEInput.DragDrop += new System.Windows.Forms.DragEventHandler(this.textBox2_DragDrop);
            this.textBoxUEInput.DragOver += new System.Windows.Forms.DragEventHandler(this.textBox2_DragOver);
            // 
            // textBoxOutput
            // 
            this.textBoxOutput.Location = new System.Drawing.Point(177, 71);
            this.textBoxOutput.Name = "textBoxOutput";
            this.textBoxOutput.PlaceholderText = "Select Output Path";
            this.textBoxOutput.Size = new System.Drawing.Size(418, 23);
            this.textBoxOutput.TabIndex = 3;
            // 
            // button1
            // 
            this.button1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.button1.Location = new System.Drawing.Point(601, 13);
            this.button1.Name = "button1";
            this.button1.Size = new System.Drawing.Size(27, 23);
            this.button1.TabIndex = 4;
            this.button1.Text = "...";
            this.button1.UseVisualStyleBackColor = true;
            this.button1.Click += new System.EventHandler(this.button1_Click);
            // 
            // button2
            // 
            this.button2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.button2.Location = new System.Drawing.Point(601, 43);
            this.button2.Name = "button2";
            this.button2.Size = new System.Drawing.Size(27, 23);
            this.button2.TabIndex = 5;
            this.button2.Text = "...";
            this.button2.UseVisualStyleBackColor = true;
            this.button2.Click += new System.EventHandler(this.button2_Click);
            // 
            // buttonSInject
            // 
            this.buttonSInject.ForeColor = System.Drawing.SystemColors.ControlText;
            this.buttonSInject.Location = new System.Drawing.Point(3, 3);
            this.buttonSInject.Name = "buttonSInject";
            this.buttonSInject.Size = new System.Drawing.Size(418, 34);
            this.buttonSInject.TabIndex = 7;
            this.buttonSInject.Text = "Start Injection";
            this.buttonSInject.UseVisualStyleBackColor = true;
            this.buttonSInject.Click += new System.EventHandler(this.button4_Click);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BackColor = System.Drawing.SystemColors.ControlLight;
            this.label1.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label1.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label1.Location = new System.Drawing.Point(31, 16);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(140, 17);
            this.label1.TabIndex = 8;
            this.label1.Text = "Select 7R Input .uexp File";
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.SystemColors.ControlLight;
            this.label2.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label2.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label2.Location = new System.Drawing.Point(23, 46);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(148, 17);
            this.label2.TabIndex = 9;
            this.label2.Text = "Select 4.18 Input .uexp File";
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.BackColor = System.Drawing.SystemColors.ControlLight;
            this.label3.BorderStyle = System.Windows.Forms.BorderStyle.Fixed3D;
            this.label3.ForeColor = System.Drawing.SystemColors.ControlText;
            this.label3.Location = new System.Drawing.Point(63, 74);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(108, 17);
            this.label3.TabIndex = 10;
            this.label3.Text = "Select Output Path";
            // 
            // button3
            // 
            this.button3.ForeColor = System.Drawing.SystemColors.ControlText;
            this.button3.Location = new System.Drawing.Point(601, 71);
            this.button3.Name = "button3";
            this.button3.Size = new System.Drawing.Size(27, 23);
            this.button3.TabIndex = 11;
            this.button3.Text = "...";
            this.button3.UseVisualStyleBackColor = true;
            this.button3.Click += new System.EventHandler(this.button3_Click);
            // 
            // menuStrip1
            // 
            this.menuStrip1.Items.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.fileToolStripMenuItem});
            this.menuStrip1.Location = new System.Drawing.Point(0, 0);
            this.menuStrip1.Name = "menuStrip1";
            this.menuStrip1.Size = new System.Drawing.Size(800, 24);
            this.menuStrip1.TabIndex = 12;
            this.menuStrip1.Text = "menuStrip1";
            // 
            // fileToolStripMenuItem
            // 
            this.fileToolStripMenuItem.DropDownItems.AddRange(new System.Windows.Forms.ToolStripItem[] {
            this.savePathSettingsToolStripMenuItem,
            this.aboutToolStripMenuItem});
            this.fileToolStripMenuItem.Name = "fileToolStripMenuItem";
            this.fileToolStripMenuItem.Size = new System.Drawing.Size(37, 20);
            this.fileToolStripMenuItem.Text = "File";
            // 
            // savePathSettingsToolStripMenuItem
            // 
            this.savePathSettingsToolStripMenuItem.Name = "savePathSettingsToolStripMenuItem";
            this.savePathSettingsToolStripMenuItem.Size = new System.Drawing.Size(193, 22);
            this.savePathSettingsToolStripMenuItem.Text = "Save Paths and Author";
            this.savePathSettingsToolStripMenuItem.Click += new System.EventHandler(this.savePathSettingsToolStripMenuItem_Click);
            // 
            // aboutToolStripMenuItem
            // 
            this.aboutToolStripMenuItem.Name = "aboutToolStripMenuItem";
            this.aboutToolStripMenuItem.Size = new System.Drawing.Size(193, 22);
            this.aboutToolStripMenuItem.Text = "About";
            this.aboutToolStripMenuItem.Click += new System.EventHandler(this.aboutToolStripMenuItem_Click);
            // 
            // radioButton1
            // 
            this.radioButton1.AutoSize = true;
            this.radioButton1.Checked = true;
            this.radioButton1.Location = new System.Drawing.Point(6, 22);
            this.radioButton1.Name = "radioButton1";
            this.radioButton1.Size = new System.Drawing.Size(99, 19);
            this.radioButton1.TabIndex = 15;
            this.radioButton1.TabStop = true;
            this.radioButton1.Text = "FF7R Injection";
            this.radioButton1.UseVisualStyleBackColor = true;
            this.radioButton1.CheckedChanged += new System.EventHandler(this.radioButton1_CheckedChanged);
            // 
            // radioButton2
            // 
            this.radioButton2.AutoSize = true;
            this.radioButton2.Location = new System.Drawing.Point(141, 22);
            this.radioButton2.Name = "radioButton2";
            this.radioButton2.Size = new System.Drawing.Size(151, 19);
            this.radioButton2.TabIndex = 16;
            this.radioButton2.Text = "UE 4.18 Dump / Validate";
            this.radioButton2.UseVisualStyleBackColor = true;
            this.radioButton2.CheckedChanged += new System.EventHandler(this.radioButton2_CheckedChanged);
            // 
            // groupBoxAppMode
            // 
            this.groupBoxAppMode.Controls.Add(this.radioButton1);
            this.groupBoxAppMode.Controls.Add(this.radioButton2);
            this.groupBoxAppMode.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.groupBoxAppMode.Location = new System.Drawing.Point(189, 27);
            this.groupBoxAppMode.Name = "groupBoxAppMode";
            this.groupBoxAppMode.Size = new System.Drawing.Size(418, 51);
            this.groupBoxAppMode.TabIndex = 17;
            this.groupBoxAppMode.TabStop = false;
            this.groupBoxAppMode.Text = "Mode";
            // 
            // groupBox7RInject
            // 
            this.groupBox7RInject.Controls.Add(this.authorlabel4);
            this.groupBox7RInject.Controls.Add(this.authortextBox1);
            this.groupBox7RInject.Controls.Add(this.radioButtonMdValid);
            this.groupBox7RInject.Controls.Add(this.radioButtonMdDump);
            this.groupBox7RInject.Controls.Add(this.radioButtonMdLODs);
            this.groupBox7RInject.Controls.Add(this.radioButtonMdInject);
            this.groupBox7RInject.Controls.Add(this.checkedListBox7ROpt);
            this.groupBox7RInject.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.groupBox7RInject.Location = new System.Drawing.Point(3, 3);
            this.groupBox7RInject.Name = "groupBox7RInject";
            this.groupBox7RInject.Size = new System.Drawing.Size(418, 200);
            this.groupBox7RInject.TabIndex = 18;
            this.groupBox7RInject.TabStop = false;
            this.groupBox7RInject.Text = "FF7R Injection Options";
            // 
            // authorlabel4
            // 
            this.authorlabel4.AutoSize = true;
            this.authorlabel4.Location = new System.Drawing.Point(7, 169);
            this.authorlabel4.Name = "authorlabel4";
            this.authorlabel4.Size = new System.Drawing.Size(200, 15);
            this.authorlabel4.TabIndex = 6;
            this.authorlabel4.Text = "Add Authorship Metadata to Import:";
            // 
            // authortextBox1
            // 
            this.authortextBox1.Font = new System.Drawing.Font("Segoe UI", 8F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.authortextBox1.Location = new System.Drawing.Point(207, 167);
            this.authortextBox1.Name = "authortextBox1";
            this.authortextBox1.Size = new System.Drawing.Size(193, 22);
            this.authortextBox1.TabIndex = 5;
            // 
            // radioButtonMdValid
            // 
            this.radioButtonMdValid.AutoSize = true;
            this.radioButtonMdValid.Location = new System.Drawing.Point(6, 66);
            this.radioButtonMdValid.Name = "radioButtonMdValid";
            this.radioButtonMdValid.Size = new System.Drawing.Size(66, 19);
            this.radioButtonMdValid.TabIndex = 4;
            this.radioButtonMdValid.TabStop = true;
            this.radioButtonMdValid.Text = "Validate";
            this.radioButtonMdValid.UseVisualStyleBackColor = true;
            this.radioButtonMdValid.CheckedChanged += new System.EventHandler(this.radioButtonMdValid_CheckedChanged);
            // 
            // radioButtonMdDump
            // 
            this.radioButtonMdDump.AutoSize = true;
            this.radioButtonMdDump.Location = new System.Drawing.Point(6, 91);
            this.radioButtonMdDump.Name = "radioButtonMdDump";
            this.radioButtonMdDump.Size = new System.Drawing.Size(98, 19);
            this.radioButtonMdDump.TabIndex = 3;
            this.radioButtonMdDump.TabStop = true;
            this.radioButtonMdDump.Text = "Dump Buffers";
            this.radioButtonMdDump.UseVisualStyleBackColor = true;
            this.radioButtonMdDump.CheckedChanged += new System.EventHandler(this.radioButtonMdDump_CheckedChanged);
            // 
            // radioButtonMdLODs
            // 
            this.radioButtonMdLODs.AutoSize = true;
            this.radioButtonMdLODs.Location = new System.Drawing.Point(6, 41);
            this.radioButtonMdLODs.Name = "radioButtonMdLODs";
            this.radioButtonMdLODs.Size = new System.Drawing.Size(177, 19);
            this.radioButtonMdLODs.TabIndex = 2;
            this.radioButtonMdLODs.TabStop = true;
            this.radioButtonMdLODs.Text = "Remove LODs (Except LOD0)";
            this.radioButtonMdLODs.UseVisualStyleBackColor = true;
            this.radioButtonMdLODs.CheckedChanged += new System.EventHandler(this.radioButtonMdLODs_CheckedChanged);
            // 
            // radioButtonMdInject
            // 
            this.radioButtonMdInject.AutoSize = true;
            this.radioButtonMdInject.Location = new System.Drawing.Point(6, 18);
            this.radioButtonMdInject.Name = "radioButtonMdInject";
            this.radioButtonMdInject.Size = new System.Drawing.Size(54, 19);
            this.radioButtonMdInject.TabIndex = 1;
            this.radioButtonMdInject.TabStop = true;
            this.radioButtonMdInject.Text = "Inject";
            this.radioButtonMdInject.UseVisualStyleBackColor = true;
            this.radioButtonMdInject.CheckedChanged += new System.EventHandler(this.radioButtonMdInject_CheckedChanged);
            // 
            // checkedListBox7ROpt
            // 
            this.checkedListBox7ROpt.CheckOnClick = true;
            this.checkedListBox7ROpt.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point);
            this.checkedListBox7ROpt.FormattingEnabled = true;
            this.checkedListBox7ROpt.Items.AddRange(new object[] {
            "Import Bones (Experimental)",
            "Keep KDI (Not recommended)"});
            this.checkedListBox7ROpt.Location = new System.Drawing.Point(6, 121);
            this.checkedListBox7ROpt.Name = "checkedListBox7ROpt";
            this.checkedListBox7ROpt.Size = new System.Drawing.Size(394, 40);
            this.checkedListBox7ROpt.TabIndex = 0;
            // 
            // groupBoxUEOpt
            // 
            this.groupBoxUEOpt.Controls.Add(this.radioButtonUEModeValid);
            this.groupBoxUEOpt.Controls.Add(this.radioButtonUEModeDump);
            this.groupBoxUEOpt.ForeColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.groupBoxUEOpt.Location = new System.Drawing.Point(3, 209);
            this.groupBoxUEOpt.Name = "groupBoxUEOpt";
            this.groupBoxUEOpt.Size = new System.Drawing.Size(418, 167);
            this.groupBoxUEOpt.TabIndex = 19;
            this.groupBoxUEOpt.TabStop = false;
            this.groupBoxUEOpt.Text = "UE 4.18 Validation Options";
            this.groupBoxUEOpt.Visible = false;
            // 
            // radioButtonUEModeValid
            // 
            this.radioButtonUEModeValid.AutoSize = true;
            this.radioButtonUEModeValid.Location = new System.Drawing.Point(6, 22);
            this.radioButtonUEModeValid.Name = "radioButtonUEModeValid";
            this.radioButtonUEModeValid.Size = new System.Drawing.Size(66, 19);
            this.radioButtonUEModeValid.TabIndex = 1;
            this.radioButtonUEModeValid.TabStop = true;
            this.radioButtonUEModeValid.Text = "Validate";
            this.radioButtonUEModeValid.UseVisualStyleBackColor = true;
            // 
            // radioButtonUEModeDump
            // 
            this.radioButtonUEModeDump.AutoSize = true;
            this.radioButtonUEModeDump.Location = new System.Drawing.Point(6, 47);
            this.radioButtonUEModeDump.Name = "radioButtonUEModeDump";
            this.radioButtonUEModeDump.Size = new System.Drawing.Size(98, 19);
            this.radioButtonUEModeDump.TabIndex = 0;
            this.radioButtonUEModeDump.TabStop = true;
            this.radioButtonUEModeDump.Text = "Dump Buffers";
            this.radioButtonUEModeDump.UseVisualStyleBackColor = true;
            // 
            // flowLayoutPanel1
            // 
            this.flowLayoutPanel1.Controls.Add(this.groupBox7RInject);
            this.flowLayoutPanel1.Controls.Add(this.groupBoxUEOpt);
            this.flowLayoutPanel1.Location = new System.Drawing.Point(189, 189);
            this.flowLayoutPanel1.Name = "flowLayoutPanel1";
            this.flowLayoutPanel1.Size = new System.Drawing.Size(425, 207);
            this.flowLayoutPanel1.TabIndex = 20;
            // 
            // groupBox1
            // 
            this.groupBox1.Controls.Add(this.label1);
            this.groupBox1.Controls.Add(this.label2);
            this.groupBox1.Controls.Add(this.label3);
            this.groupBox1.Controls.Add(this.button3);
            this.groupBox1.Controls.Add(this.textBoxOutput);
            this.groupBox1.Controls.Add(this.textBox7RInput);
            this.groupBox1.Controls.Add(this.button2);
            this.groupBox1.Controls.Add(this.textBoxUEInput);
            this.groupBox1.Controls.Add(this.button1);
            this.groupBox1.Location = new System.Drawing.Point(87, 83);
            this.groupBox1.Name = "groupBox1";
            this.groupBox1.Size = new System.Drawing.Size(636, 100);
            this.groupBox1.TabIndex = 21;
            this.groupBox1.TabStop = false;
            this.groupBox1.Text = "Paths";
            // 
            // flowLayoutPanel2
            // 
            this.flowLayoutPanel2.Controls.Add(this.buttonSInject);
            this.flowLayoutPanel2.Location = new System.Drawing.Point(189, 413);
            this.flowLayoutPanel2.Name = "flowLayoutPanel2";
            this.flowLayoutPanel2.Size = new System.Drawing.Size(425, 47);
            this.flowLayoutPanel2.TabIndex = 22;
            // 
            // richTextBox1
            // 
            this.richTextBox1.BackColor = System.Drawing.SystemColors.ActiveCaptionText;
            this.richTextBox1.ForeColor = System.Drawing.SystemColors.HighlightText;
            this.richTextBox1.ImeMode = System.Windows.Forms.ImeMode.NoControl;
            this.richTextBox1.Location = new System.Drawing.Point(195, 463);
            this.richTextBox1.Name = "richTextBox1";
            this.richTextBox1.ReadOnly = true;
            this.richTextBox1.ScrollBars = System.Windows.Forms.RichTextBoxScrollBars.ForcedVertical;
            this.richTextBox1.Size = new System.Drawing.Size(412, 41);
            this.richTextBox1.TabIndex = 24;
            this.richTextBox1.Text = "";
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackColor = System.Drawing.SystemColors.Control;
            this.ClientSize = new System.Drawing.Size(800, 520);
            this.Controls.Add(this.richTextBox1);
            this.Controls.Add(this.flowLayoutPanel2);
            this.Controls.Add(this.groupBox1);
            this.Controls.Add(this.flowLayoutPanel1);
            this.Controls.Add(this.groupBoxAppMode);
            this.Controls.Add(this.menuStrip1);
            this.ForeColor = System.Drawing.SystemColors.ControlLightLight;
            this.MainMenuStrip = this.menuStrip1;
            this.Name = "Form1";
            this.Text = "FF7R Model UEXP Injector";
            this.menuStrip1.ResumeLayout(false);
            this.menuStrip1.PerformLayout();
            this.groupBoxAppMode.ResumeLayout(false);
            this.groupBoxAppMode.PerformLayout();
            this.groupBox7RInject.ResumeLayout(false);
            this.groupBox7RInject.PerformLayout();
            this.groupBoxUEOpt.ResumeLayout(false);
            this.groupBoxUEOpt.PerformLayout();
            this.flowLayoutPanel1.ResumeLayout(false);
            this.groupBox1.ResumeLayout(false);
            this.groupBox1.PerformLayout();
            this.flowLayoutPanel2.ResumeLayout(false);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion
        private TextBox textBox7RInput;
        private TextBox textBoxUEInput;
        private TextBox textBoxOutput;
        private Button button1;
        private Button button2;
        private Button button3;
        private Button buttonSInject;
        private Label label1;
        private Label label2;
        private Label label3;
        private MenuStrip menuStrip1;
        private ToolStripMenuItem fileToolStripMenuItem;
        private ToolStripMenuItem savePathSettingsToolStripMenuItem;
        private ToolStripMenuItem aboutToolStripMenuItem;
        private RadioButton radioButton1;
        private RadioButton radioButton2;
        private GroupBox groupBoxAppMode;
        private GroupBox groupBox7RInject;
        private RadioButton radioButtonMdValid;
        private RadioButton radioButtonMdDump;
        private RadioButton radioButtonMdLODs;
        private RadioButton radioButtonMdInject;
        private CheckedListBox checkedListBox7ROpt;
        private GroupBox groupBoxUEOpt;
        private RadioButton radioButtonUEModeValid;
        private RadioButton radioButtonUEModeDump;
        private FlowLayoutPanel flowLayoutPanel1;
        private GroupBox groupBox1;
        private FlowLayoutPanel flowLayoutPanel2;
        private RichTextBox resultTextBox;
        private FontDialog fontDialog1;
        private RichTextBox richTextBox1;
        private Label authorlabel4;
        private TextBox authortextBox1;
    }
}