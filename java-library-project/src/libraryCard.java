// LibraryCard.java - بعد التعديلات المطلوبة:
// 1. إضافة ComboBox لعرض Member IDs
// 2. جعل تاريخ الانتهاء باستخدام JDateChooser بدلاً من JTextField

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;
import com.toedter.calendar.JDateChooser;
import java.util.Date;

public class libraryCard {

    private JTextField txtId;
    private JComboBox<String> membershipBox, memberIdBox;
    private JDateChooser expiryDateChooser;
    private JTable table;
    private DefaultTableModel model;

    public JPanel getPanel(Connection conn) {
        JPanel panel = new JPanel();
        panel.setLayout(null);

        JLabel label = new JLabel("Library Card Management");
        label.setFont(new Font("Tahoma", Font.BOLD, 20));
        label.setBounds(250, 10, 400, 30);
        panel.add(label);

        JLabel lblId = new JLabel("Card ID:");
        lblId.setBounds(30, 60, 100, 25);
        panel.add(lblId);

        txtId = new JTextField();
        txtId.setBounds(150, 60, 150, 25);
        panel.add(txtId);

        JLabel lblType = new JLabel("Membership Type:");
        lblType.setBounds(30, 100, 120, 25);
        panel.add(lblType);

        membershipBox = new JComboBox<>(new String[]{"Student", "Employee", "Researcher", "Premium"});
        membershipBox.setBounds(150, 100, 150, 25);
        panel.add(membershipBox);

        JLabel lblMemberId = new JLabel("Member ID:");
        lblMemberId.setBounds(30, 140, 100, 25);
        panel.add(lblMemberId);

        memberIdBox = new JComboBox<>();
        memberIdBox.setBounds(150, 140, 150, 25);
        panel.add(memberIdBox);

        JLabel lblExpiry = new JLabel("Expiry Date:");
        lblExpiry.setBounds(30, 180, 100, 25);
        panel.add(lblExpiry);

        expiryDateChooser = new JDateChooser();
        expiryDateChooser.setDateFormatString("yyyy-MM-dd");
        expiryDateChooser.setBounds(150, 180, 150, 25);
        panel.add(expiryDateChooser);

        JButton insertBtn = new JButton("Insert");
        insertBtn.setBounds(30, 230, 80, 30);
        panel.add(insertBtn);

        JButton updateBtn = new JButton("Update");
        updateBtn.setBounds(120, 230, 80, 30);
        panel.add(updateBtn);

        JButton deleteBtn = new JButton("Delete");
        deleteBtn.setBounds(210, 230, 80, 30);
        panel.add(deleteBtn);

        model = new DefaultTableModel(new String[]{"Card ID", "Membership Type", "Member ID", "Expiry Date"}, 0);
        table = new JTable(model);
        JScrollPane scroll = new JScrollPane(table);
        scroll.setBounds(330, 60, 600, 300);
        panel.add(scroll);

        loadMembers(conn);
        loadData(conn);

        insertBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement(
                        "INSERT INTO library_card (card_id, membership_type, member_id, expiry_date) VALUES (?, ?, ?, ?)"
                    );
                    ps.setInt(1, Integer.parseInt(txtId.getText()));
                    ps.setString(2, membershipBox.getSelectedItem().toString());
                    ps.setInt(3, Integer.parseInt(memberIdBox.getSelectedItem().toString()));
                    Date date = expiryDateChooser.getDate();
                    if (date == null) {
                        JOptionPane.showMessageDialog(panel, "Please select a valid expiry date.");
                        return;
                    }
                    ps.setDate(4, new java.sql.Date(date.getTime()));
                    ps.executeUpdate();
                    loadData(conn);
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Insert failed: " + ex.getMessage());
                }
            }
        });

        updateBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement(
                        "UPDATE library_card SET membership_type=?, member_id=?, expiry_date=? WHERE card_id=?"
                    );
                    ps.setString(1, membershipBox.getSelectedItem().toString());
                    ps.setInt(2, Integer.parseInt(memberIdBox.getSelectedItem().toString()));
                    Date date = expiryDateChooser.getDate();
                    if (date == null) {
                        JOptionPane.showMessageDialog(panel, "Please select a valid expiry date.");
                        return;
                    }
                    ps.setDate(3, new java.sql.Date(date.getTime()));
                    ps.setInt(4, Integer.parseInt(txtId.getText()));
                    ps.executeUpdate();
                    loadData(conn);
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Update failed.");
                }
            }
        });

        deleteBtn.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement(
                        "DELETE FROM library_card WHERE card_id=?"
                    );
                    ps.setInt(1, Integer.parseInt(txtId.getText()));
                    ps.executeUpdate();
                    loadData(conn);
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Delete failed.");
                }
            }
        });
        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int row = table.getSelectedRow();
                txtId.setText(model.getValueAt(row, 0).toString());
                membershipBox.setSelectedItem(model.getValueAt(row, 1).toString());
                memberIdBox.setSelectedItem(model.getValueAt(row, 2).toString());
                try {
                    java.util.Date date = java.sql.Date.valueOf(model.getValueAt(row, 3).toString());
                    expiryDateChooser.setDate(date);
                } catch (Exception ex) {
                    expiryDateChooser.setDate(null);
                }
            }
        });

        
        JButton refresh = new JButton("Refresh");
        refresh.setBounds(650, 400, 100, 30); // زر تحديث بجانب العناصر
        panel.add(refresh);

        refresh.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                loadMembers(conn); // تحديث قائمة الأعضاء
                loadData(conn); // تحديث جدول البطاقات
            }
        });

        
        return panel;
    }

    private void loadData(Connection conn) {
        try {
            model.setRowCount(0);
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM library_card");
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getInt("card_id"),
                    rs.getString("membership_type"),
                    rs.getInt("member_id"),
                    rs.getString("expiry_date")
                });
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void loadMembers(Connection conn) {
        try {
            memberIdBox.removeAllItems();
            PreparedStatement ps = conn.prepareStatement("SELECT member_id FROM member");
            ResultSet rs = ps.executeQuery();
            while (rs.next()) {
                memberIdBox.addItem(rs.getString("member_id"));
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}
