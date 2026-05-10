import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class MemberWindow {

	private JTextField txtId, txtName, txtEmail, txtPhone;
	private JTable table;
	private DefaultTableModel model;

	public JPanel getPanel(Connection conn) {
		JPanel panel = new JPanel();
		panel.setLayout(null);

		JLabel label = new JLabel("Member Management");
		label.setFont(new Font("Tahoma", Font.BOLD, 20));
		label.setBounds(300, 10, 300, 30);
		panel.add(label);

		JLabel lblId = new JLabel("Member ID:");
		lblId.setBounds(30, 60, 100, 25);
		panel.add(lblId);

		txtId = new JTextField();
		txtId.setBounds(130, 60, 150, 25);
		panel.add(txtId);

		JLabel lblName = new JLabel("Name:");
		lblName.setBounds(30, 100, 100, 25);
		panel.add(lblName);

		txtName = new JTextField();
		txtName.setBounds(130, 100, 150, 25);
		panel.add(txtName);

		JLabel lblEmail = new JLabel("Email:");
		lblEmail.setBounds(30, 140, 100, 25);
		panel.add(lblEmail);

		txtEmail = new JTextField();
		txtEmail.setBounds(130, 140, 150, 25);
		panel.add(txtEmail);

		JLabel lblPhone = new JLabel("Phone:");
		lblPhone.setBounds(30, 180, 100, 25);
		panel.add(lblPhone);

		txtPhone = new JTextField();
		txtPhone.setBounds(130, 180, 150, 25);
		panel.add(txtPhone);

		JButton insertBtn = new JButton("Insert");
		insertBtn.setBounds(30, 220, 80, 30);
		panel.add(insertBtn);

		JButton updateBtn = new JButton("Update");
		updateBtn.setBounds(120, 220, 80, 30);
		panel.add(updateBtn);

		JButton deleteBtn = new JButton("Delete");
		deleteBtn.setBounds(210, 220, 80, 30);
		panel.add(deleteBtn);

		model = new DefaultTableModel(new String[]{"ID", "Name", "Email", "Phone"}, 0);
		table = new JTable(model);
		JScrollPane scroll = new JScrollPane(table);
		scroll.setBounds(320, 60, 600, 300);
		panel.add(scroll);

		loadData(conn);

		insertBtn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					PreparedStatement ps = conn.prepareStatement("INSERT INTO member (member_id, name, email, phone_number) VALUES (?, ?, ?, ?)");
					ps.setInt(1, Integer.parseInt(txtId.getText()));
					ps.setString(2, txtName.getText());
					ps.setString(3, txtEmail.getText());
					ps.setString(4, txtPhone.getText());
					ps.executeUpdate();
					loadData(conn);
					JOptionPane.showMessageDialog(panel, "Member Inserted!");
				} catch (Exception ex) {
					ex.printStackTrace();
					JOptionPane.showMessageDialog(panel, "Insert failed: " + ex.getMessage());
				}
			}
		});

		updateBtn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					PreparedStatement ps = conn.prepareStatement("UPDATE member SET name=?, email=?, phone_number=? WHERE member_id=?");
					ps.setString(1, txtName.getText());
					ps.setString(2, txtEmail.getText());
					ps.setString(3, txtPhone.getText());
					ps.setInt(4, Integer.parseInt(txtId.getText()));
					ps.executeUpdate();
					loadData(conn);
					JOptionPane.showMessageDialog(panel, "Member Updated!"); 
				} catch (Exception ex) {
					ex.printStackTrace();
					JOptionPane.showMessageDialog(panel, "Update failed: " + ex.getMessage());
				}
			}
		});

		deleteBtn.addActionListener(new ActionListener() {
			public void actionPerformed(ActionEvent e) {
				try {
					PreparedStatement ps = conn.prepareStatement("DELETE FROM member WHERE member_id=?");
					ps.setInt(1, Integer.parseInt(txtId.getText()));
					ps.executeUpdate();
					loadData(conn);
					JOptionPane.showMessageDialog(panel, "Member Deleted!");
				} catch (Exception ex) {
					ex.printStackTrace();
					JOptionPane.showMessageDialog(panel, "Delete failed: " + ex.getMessage());
				}
			}
		});

		table.addMouseListener(new MouseAdapter() {
			public void mouseClicked(MouseEvent e) {
				int row = table.getSelectedRow();
				txtId.setText(model.getValueAt(row, 0).toString());
				txtName.setText(model.getValueAt(row, 1).toString());
				txtEmail.setText(model.getValueAt(row, 2).toString());
				txtPhone.setText(model.getValueAt(row, 3).toString());
			}
		});

		JButton refresh = new JButton("Refresh");
		refresh.setBounds(450, 400, 100, 30); // زر تحديث بجانب الجدول
		panel.add(refresh);

		refresh.addActionListener(new ActionListener() {
		    public void actionPerformed(ActionEvent e) {
		        loadData(conn); // تحديث جدول الأعضاء
		  }
		});

		
		
		return panel;
	}

	private void loadData(Connection conn) {
		try {
			model.setRowCount(0);
			Statement stmt = conn.createStatement();
			ResultSet rs = stmt.executeQuery("SELECT * FROM member");
			while (rs.next()) {
				model.addRow(new Object[]{rs.getInt("member_id"), rs.getString("name"), rs.getString("email"), rs.getString("phone_number")});
			}
		} catch (Exception ex) {
			ex.printStackTrace();
		}
	}
}
