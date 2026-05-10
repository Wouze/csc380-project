// BookAuthorWindow.java - بعد التعديلات المطلوبة:
// - حذف جميع الأدوار ما عدا Author وCo-Author
// - البحث يكون فقط باستخدام Author ID

import java.sql.*;
import java.awt.Font;
import javax.swing.*;
import javax.swing.border.TitledBorder;
import javax.swing.table.DefaultTableModel;
import java.awt.event.*;

public class BookAuthorWindow {
    private JComboBox<String> ba_role_combo;
    private JTextField ba_search_txt;
    private JTable table;
    private JComboBox<String> ba_combo_book;
    private JComboBox<String> ba_combo_author;
    private DefaultTableModel model;

    public JPanel getPanel(Connection conn) {
        JPanel panel = new JPanel();
        panel.setLayout(null);
        panel.setBounds(0, 0, 892, 494);

        JLabel title = new JLabel("Book - Author Management");
        title.setFont(new Font("Tahoma", Font.BOLD, 30));
        title.setHorizontalAlignment(SwingConstants.CENTER);
        title.setBounds(166, 23, 501, 47);
        panel.add(title);

        JPanel info = new JPanel();
        info.setBounds(34, 84, 331, 247);
        info.setBorder(new TitledBorder("Information of Book & Author"));
        info.setLayout(null);
        panel.add(info);

        JLabel bookIdLabel = new JLabel("Book ID:");
        bookIdLabel.setFont(new Font("Tahoma", Font.PLAIN, 18));
        bookIdLabel.setBounds(25, 23, 130, 36);
        info.add(bookIdLabel);

        ba_combo_book = new JComboBox<>();
        ba_combo_book.setBounds(140, 32, 152, 25);
        info.add(ba_combo_book);

        JLabel authorIdLabel = new JLabel("Author ID:");
        authorIdLabel.setFont(new Font("Tahoma", Font.PLAIN, 18));
        authorIdLabel.setBounds(25, 70, 130, 36);
        info.add(authorIdLabel);

        ba_combo_author = new JComboBox<>();
        ba_combo_author.setBounds(140, 79, 152, 25);
        info.add(ba_combo_author);

        JLabel roleLabel = new JLabel("Role:");
        roleLabel.setFont(new Font("Tahoma", Font.PLAIN, 18));
        roleLabel.setBounds(25, 118, 130, 36);
        info.add(roleLabel);

        ba_role_combo = new JComboBox<>(new String[]{"Author", "Co-Author"});
        ba_role_combo.setBounds(140, 129, 152, 25);
        info.add(ba_role_combo);

        JButton insert = new JButton("Insert");
        insert.setBounds(25, 175, 78, 47);
        info.add(insert);

        JButton delete = new JButton("Delete");
        delete.setBounds(123, 175, 78, 47);
        info.add(delete);

        JButton update = new JButton("Update");
        update.setBounds(214, 175, 78, 47);
        info.add(update);

        JPanel search = new JPanel();
        search.setBounds(38, 342, 327, 90);
        search.setBorder(new TitledBorder("Search by Author ID"));
        search.setLayout(null);
        panel.add(search);

        JLabel searchLabel = new JLabel("Author ID:");
        searchLabel.setFont(new Font("Tahoma", Font.PLAIN, 18));
        searchLabel.setBounds(10, 22, 100, 36);
        search.add(searchLabel);

        ba_search_txt = new JTextField();
        ba_search_txt.setBounds(120, 30, 172, 25);
        search.add(ba_search_txt);

        JButton searchBtn = new JButton("Search");
        searchBtn.setBounds(20, 59, 98, 20);
        search.add(searchBtn);

        model = new DefaultTableModel(new String[]{"Book ID", "Author ID", "Role"}, 0);
        table = new JTable(model);
        JScrollPane scroll = new JScrollPane(table);
        scroll.setBounds(391, 84, 449, 348);
        panel.add(scroll);

        loadComboBoxes(conn);
        loadData(conn);

        insert.addActionListener(e -> insertBookAuthor(conn, panel));
        delete.addActionListener(e -> deleteBookAuthor(conn, panel));
        update.addActionListener(e -> updateBookAuthor(conn, panel));
        searchBtn.addActionListener(e -> searchBookAuthor(conn, panel));

        table.addMouseListener(new MouseAdapter() {
            public void mouseClicked(MouseEvent e) {
                int row = table.getSelectedRow();
                if (row >= 0) {
                    ba_combo_book.setSelectedItem(model.getValueAt(row, 0).toString());
                    ba_combo_author.setSelectedItem(model.getValueAt(row, 1).toString());
                    ba_role_combo.setSelectedItem(model.getValueAt(row, 2).toString());
                }
            }
        });
        
        JButton refresh = new JButton("Refresh");
        refresh.setBounds(380, 440, 100, 30); // زر في الأسفل بجانب بقية العناصر
        panel.add(refresh);

        refresh.addActionListener(new ActionListener() {
           
            public void actionPerformed(ActionEvent e) {
                loadComboBoxes(conn); // تحديث قائمة الكتب والمؤلفين
                loadData(conn); // تحديث الجدول 
            }
        });


        return panel;
    }

    public void loadComboBoxes(Connection conn) {
        try {
            ba_combo_book.removeAllItems();
            ba_combo_author.removeAllItems();
            Statement bookStmt = conn.createStatement();
            ResultSet books = bookStmt.executeQuery("SELECT book_id FROM book");
            while (books.next()) ba_combo_book.addItem(books.getString("book_id"));

            Statement authorStmt = conn.createStatement();
            ResultSet authors = authorStmt.executeQuery("SELECT author_id FROM author");
            while (authors.next()) ba_combo_author.addItem(authors.getString("author_id"));

        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void loadData(Connection conn) {
        try {
            model.setRowCount(0);
            Statement stmt = conn.createStatement();
            ResultSet rs = stmt.executeQuery("SELECT * FROM book_author");
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getString("book_id"),
                    rs.getString("author_id"),
                    rs.getString("role")
                });
            }
        } catch (Exception ex) {
            ex.printStackTrace();
        }
    }

    private void insertBookAuthor(Connection conn, JPanel panel) {
        try {
            String bookId = (String) ba_combo_book.getSelectedItem();
            String authorId = (String) ba_combo_author.getSelectedItem();
            String role = (String) ba_role_combo.getSelectedItem();

            PreparedStatement ps = conn.prepareStatement(
                "INSERT INTO book_author (book_id, author_id, role) VALUES (?, ?, ?)");
            ps.setInt(1, Integer.parseInt(bookId));
            ps.setInt(2, Integer.parseInt(authorId));
            ps.setString(3, role);
            ps.executeUpdate();

            JOptionPane.showMessageDialog(panel, "Inserted successfully");
            loadData(conn);
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(panel, "Insert failed: " + ex.getMessage());
        }
    }

    private void deleteBookAuthor(Connection conn, JPanel panel) {
        try {
            String bookId = (String) ba_combo_book.getSelectedItem();
            String authorId = (String) ba_combo_author.getSelectedItem();

            PreparedStatement ps = conn.prepareStatement(
                "DELETE FROM book_author WHERE book_id = ? AND author_id = ?");
            ps.setInt(1, Integer.parseInt(bookId));
            ps.setInt(2, Integer.parseInt(authorId));
            int rows = ps.executeUpdate();

            if (rows > 0) {
                JOptionPane.showMessageDialog(panel, "Deleted successfully");
                loadData(conn);
            } else {
                JOptionPane.showMessageDialog(panel, "Not found");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(panel, "Delete failed: " + ex.getMessage());
        }
    }

    private void updateBookAuthor(Connection conn, JPanel panel) {
        try {
            String bookId = (String) ba_combo_book.getSelectedItem();
            String authorId = (String) ba_combo_author.getSelectedItem();
            String role = (String) ba_role_combo.getSelectedItem();

            PreparedStatement ps = conn.prepareStatement(
                "UPDATE book_author SET role = ? WHERE book_id = ? AND author_id = ?");
            ps.setString(1, role);
            ps.setInt(2, Integer.parseInt(bookId));
            ps.setInt(3, Integer.parseInt(authorId));

            int rows = ps.executeUpdate();
            if (rows > 0) {
                JOptionPane.showMessageDialog(panel, "Updated successfully");
                loadData(conn);
            } else {
                JOptionPane.showMessageDialog(panel, "Not found");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(panel, "Update failed: " + ex.getMessage());
        }
    }

    private void searchBookAuthor(Connection conn, JPanel panel) {
        try {
            String searchId = ba_search_txt.getText().trim();
            if (searchId.isEmpty()) {
                JOptionPane.showMessageDialog(panel, "Enter Author ID to search");
                return;
            }
            PreparedStatement ps = conn.prepareStatement("SELECT * FROM book_author WHERE author_id = ?");
            ps.setInt(1, Integer.parseInt(searchId));
            ResultSet rs = ps.executeQuery();

            model.setRowCount(0);
            while (rs.next()) {
                model.addRow(new Object[]{
                    rs.getString("book_id"),
                    rs.getString("author_id"),
                    rs.getString("role")
                });
            }
            if (model.getRowCount() == 0) {
                JOptionPane.showMessageDialog(panel, "No records found");
            }
        } catch (Exception ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(panel, "Search failed: " + ex.getMessage());
        }
    }
}
