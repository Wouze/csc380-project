// Author.java - النسخة الكاملة بعد تعديل الحذف لتحديث كومبو بوكس BookAuthorWindow تلقائياً

import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.*;
import java.awt.event.*;
import java.sql.*;

public class Author {
    private JTextField txtId, txtName, txtSearch;
    private JTable table;
    private DefaultTableModel model;

    public JPanel getPanel(Connection conn) {
        JPanel panel = new JPanel();
        panel.setLayout(null);

        JLabel label = new JLabel("Author Management");
        label.setFont(new Font("Tahoma", Font.BOLD, 20));
        label.setBounds(300, 10, 400, 30);
        panel.add(label);

        JPanel formPanel = new JPanel();
        formPanel.setLayout(null);
        formPanel.setBorder(new TitledBorder("Author Info"));
        formPanel.setBounds(30, 60, 300, 200);
        panel.add(formPanel);

        JLabel lblId = new JLabel("Author ID:");
        lblId.setBounds(20, 30, 100, 25);
        formPanel.add(lblId);

        txtId = new JTextField();
        txtId.setBounds(120, 30, 150, 25);
        formPanel.add(txtId);

        JLabel lblName = new JLabel("Name:");
        lblName.setBounds(20, 70, 100, 25);
        formPanel.add(lblName);

        txtName = new JTextField();
        txtName.setBounds(120, 70, 150, 25);
        formPanel.add(txtName);

        JButton insert = new JButton("Insert");
        insert.setBounds(20, 120, 80, 30);
        formPanel.add(insert);

        JButton update = new JButton("Update");
        update.setBounds(110, 120, 80, 30);
        formPanel.add(update);

        JButton delete = new JButton("Delete");
        delete.setBounds(200, 120, 80, 30);
        formPanel.add(delete);

        JPanel searchPanel = new JPanel();
        searchPanel.setLayout(null);
        searchPanel.setBorder(new TitledBorder("Search"));
        searchPanel.setBounds(30, 270, 300, 80);
        panel.add(searchPanel);

        JLabel lblSearch = new JLabel("Search by ID:");
        lblSearch.setBounds(10, 30, 100, 25);
        searchPanel.add(lblSearch);

        txtSearch = new JTextField();
        txtSearch.setBounds(110, 30, 100, 25);
        searchPanel.add(txtSearch);

        JButton btnSearch = new JButton("Search");
        btnSearch.setBounds(212, 30, 80, 25);
        searchPanel.add(btnSearch);

        model = new DefaultTableModel(new String[]{"Author ID", "Name"}, 0);
        table = new JTable(model);
        JScrollPane scroll = new JScrollPane(table);
        scroll.setBounds(350, 60, 500, 300);
        panel.add(scroll);

        loadAuthors(conn);

        insert.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement("INSERT INTO author (author_id, name) VALUES (?, ?)");
                    ps.setInt(1, Integer.parseInt(txtId.getText()));
                    ps.setString(2, txtName.getText());
                    ps.executeUpdate();
                    loadAuthors(conn);
                    JOptionPane.showMessageDialog(panel, "Author inserted.");
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Insert failed: " + ex.getMessage());
                }
            }
        });

        update.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement("UPDATE author SET name=? WHERE author_id=?");
                    ps.setString(1, txtName.getText());
                    ps.setInt(2, Integer.parseInt(txtId.getText()));
                    ps.executeUpdate();
                    loadAuthors(conn);
                    JOptionPane.showMessageDialog(panel, "Author updated.");
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Update failed: " + ex.getMessage());
                }
            }
        });

        delete.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    PreparedStatement ps = conn.prepareStatement("DELETE FROM author WHERE author_id=?");
                    ps.setInt(1, Integer.parseInt(txtId.getText()));
                    ps.executeUpdate();
                    loadAuthors(conn);

                    // تحديث كومبو بوكس في BookAuthorWindow بعد الحذف
                    BookAuthorWindow baw = new BookAuthorWindow();
                    baw.loadComboBoxes(conn);

                    JOptionPane.showMessageDialog(panel, "Author deleted.");
                } catch (Exception ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(panel, "Delete failed: " + ex.getMessage());
                }
            }
        });

        btnSearch.addActionListener(new ActionListener() {
            public void actionPerformed(ActionEvent e) {
                try {
                    model.setRowCount(0);
                    PreparedStatement ps = conn.prepareStatement("SELECT * FROM author WHERE author_id = ?");
                    ps.setInt(1, Integer.parseInt(txtSearch.getText()));
                    ResultSet rs = ps.executeQuery();
                    while (rs.next()) {
                        model.addRow(new Object[]{rs.getInt("author_id"), rs.getString("name")});
                    }
                } catch (Exception ex) {
                    ex.printStackTrace();
                }
            }
        });
        JButton refresh = new JButton("Refresh");
        refresh.setBounds(500, 370, 100, 30); // زر في الأسفل بموقع مناسب
        panel.add(refresh);

        refresh.addActionListener(new ActionListener() {
            
            public void actionPerformed(ActionEvent e) {
                loadAuthors(conn); // تحديث جدول المؤلفين
            }
        });


        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int row = table.getSelectedRow();
                txtId.setText(model.getValueAt(row, 0).toString());
                txtName.setText(model.getValueAt(row, 1).toString());
            }
        });

        return panel;
    }

    private void loadAuthors(Connection conn) {
        try {
            model.setRowCount(0);
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM author");
            while (rs.next()) {
                model.addRow(new Object[]{rs.getInt("author_id"), rs.getString("name")});
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }
}